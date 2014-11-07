from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from passport.models import Timeslot, Boat, Booking, Assignment
from passport.serializers import TimeslotSerializer, BoatSerializer
import log
import json, datetime


@api_view(['GET','POST'])
def timeslots(req):
  if req.method == 'GET':
     ### Get list of timeslots for a given date
     if (req.GET.has_key('date')):
        date = datetime.datetime.strptime(req.GET['date'], '%Y-%m-%d')
        start_timestamp = int(date.strftime('%s'))
        nextdate = date + datetime.timedelta(days=1)
        end_timestamp = int(nextdate.strftime('%s'))
        timeslots = Timeslot.objects.filter(start_time__gte=start_timestamp, start_time__lt=end_timestamp)
     else:
	timeslots = Timeslot.objects.all()
     serializer = TimeslotSerializer(timeslots, many=True)
     ### Add the assigned boats list to the serialized data
     for timeslot in serializer.data:
         timeslot['id'] = timeslot['id'].replace('tslot','')
         boats = Timeslot.objects.get(pk=timeslot['id']).get_assigned_boats()
         timeslot['boats'] = boats
	 timeslot['id'] = 'tslot' + timeslot['id']
     return Response(serializer.data)
  if req.method == 'POST':
     serializer = TimeslotSerializer(data=req.DATA)
     if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


@api_view(['GET', 'POST'])
def boats(req):
  if req.method == 'GET':
     boats = Boat.objects.all()
     serializer = BoatSerializer(boats, many=True)
     return Response(serializer.data)
  elif req.method == 'POST':
     boat = BoatSerializer(data=req.DATA)
     if boat.is_valid():
	boat.save()
        return Response(boat.data, status=status.HTTP_201_CREATED)
     return Response(boat.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def assignments(req):
  if req.method == 'POST':
     data = {}
     for key, val in req.DATA.items():
	 if key == 'timeslot_id':
	    val = val.replace('tslot','')
         elif key == 'boat_id':
	    val = val.replace('boat','')
         data[key] = val
     timeslot = Timeslot.objects.get(pk=data['timeslot_id'])
     boat = Boat.objects.get(pk=data['boat_id'])
     assignment, created = Assignment.objects.get_or_create(timeslot=timeslot, boat=boat)
     if created:
        check_assignments(assignment, timeslot, boat)
        assignment.current_capacity = boat.capacity
        assignment.save()
        timeslot.update_availability()
        timeslot.save()
        return Response("Assigned boat%s to timeslot tslot%s" % (boat.id, timeslot.id), status=status.HTTP_201_CREATED)
     else:
        return Response("Boat%s is already assigned to timeslot tslot%s" % (boat.id, timeslot.id), status=status.HTTP_400_BAD_REQUEST)
	

# When doing a booking, check to see if there are other timeslots, using the same boat. Update availability on those
# timeslots if there is any overlap.
@api_view(['POST'])
def bookings(req):
  if req.method == 'POST':
     data = {}
     for key, val in req.DATA.items():
	 if key == 'timeslot_id':
	    val = val.replace('tslot','')
         data[key] = val
     timeslot = Timeslot.objects.get(pk=data['timeslot_id'])
     size = data['size']
     if size <= timeslot.availability:
        booking = Booking(timeslot=timeslot, size=size)
        booking.boat = timeslot.reserve_boat(size)
        booking.save()
        timeslot.customer_count += size
	timeslot.update_availability()
        timeslot.save()
	check_other_timeslots(timeslot, booking.boat)
        return Response("Booking done for timeslot %s, size %s" % (timeslot.transform_id(), size), status=status.HTTP_201_CREATED)
     else:
	return Response("Booking not available for timeslot %s, size %s" % (timeslot.transform_id(), size), status=status.HTTP_400_BAD_REQUEST)
     


def get_timeslots_for_day(timeslot):
  date = datetime.datetime.fromtimestamp(timeslot.start_time)
  datestr = date.strftime('%Y%m%d')
  date = datetime.datetime.strptime(datestr, '%Y%m%d')
  start_timestamp = int(date.strftime('%s'))
  nextdate = date + datetime.timedelta(days=1)
  end_timestamp = int(nextdate.strftime('%s'))
  timeslots = Timeslot.objects.filter(start_time__gte=start_timestamp, start_time__lte=end_timestamp)
  return timeslots


## Function to check other timeslots after a booking is made on a given timeslot and boat. If any time conflicts are there
## for the same boat, mark those assignments as unbookable and those timeslots unavailable.
def check_other_timeslots(inputTimeslot, boat):
  timeslots = get_timeslots_for_day(inputTimeslot)
  for t in timeslots:
      if t.id != inputTimeslot.id and boat.transform_id() in t.get_assigned_boats():
	 if t.time_overlap(inputTimeslot):
	     assignObj = Assignment.objects.get(timeslot=t, boat=boat)
	     assignObj.bookable = False
	     assignObj.save()
             t.update_availability()
 	     t.save()
           

### Function to check when new assignments are created to see if there are any time conflicts
### and bookings already made on the same boat.
### Mark those assignments as unbookable.
def check_assignments(assignment, inputTimeslot, boat):
  timeslots = get_timeslots_for_day(inputTimeslot)
  bookable = True
  for t in timeslots:
      if t.id != inputTimeslot.id:
         other_assignments = Assignment.objects.filter(timeslot=t, boat=boat)
         if other_assignments:
	    if other_assignments[0].current_capacity < boat.capacity and t.time_overlap(inputTimeslot):
               bookable = False
	       break
  assignment.bookable = bookable
  

















