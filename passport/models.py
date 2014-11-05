from django.db import models
import hashlib
from uuid import uuid4
import hashlib

# Timeslot model
class Timeslot(models.Model):
   start_time 		= models.PositiveIntegerField(unique=True)
   duration 		= models.IntegerField()
   availability 	= models.IntegerField(default = 0)
   customer_count 	= models.IntegerField(default = 0)

 
   def __unicode__(self):
     return '<id: %s, start_time: %s, duration: %s, availability: %s, customer_count: %s, boats: %s' % (self.transform_id(), self.start_time, self.duration, self.availability, self.customer_count, self.get_assigned_boats())


   def transform_id(self):
       return 'tslot' + str(self.id)
   

   def get_assigned_boats(self):
     boats = []
     for assignmentObj in self.assignment_set.all():
         boats.append(assignmentObj.boat.transform_id())
     return boats


   def update_availability(self): 
     curr_boat_capacities = []
     for assignment in self.assignment_set.all():
	 if assignment.bookable:
            curr_boat_capacities.append(assignment.current_capacity)
     if curr_boat_capacities == []:
	self.availability = 0
     else:
        self.availability = max(curr_boat_capacities)
     

   ### Return first available boat in the list of assignments for the timeslot
   def reserve_boat(self, size):
      for assignment in self.assignment_set.all():
          if assignment.current_capacity >= size and assignment.bookable:
	     boat = assignment.boat
	     assignment.current_capacity -=  size
	     assignment.save()     
	     return boat


   def time_overlap(self, other):
       other_end_time = other.start_time + other.duration*60
       end_time = self.start_time + self.duration*60
       if (other.start_time >= self.start_time and other.start_time < end_time) or (self.start_time >= other.start_time and self.start_time < other_end_time):
	  return True
       else:
	  return False



# Boat model
class Boat(models.Model):
   name		= models.CharField(max_length=255, unique=True)
   capacity 	= models.IntegerField()

   def __unicode__(self):
     return '<id: %s, name: %s, capacity: %s>' % (self.id, self.name, self.capacity)

   def transform_id(self):
     return 'boat' + str(self.id)


#Assignment model
class Assignment(models.Model):
   timeslot = models.ForeignKey(Timeslot)
   boat = models.ForeignKey(Boat)
   ### Field for current capacity of the boat for this timeslot assignment
   current_capacity = models.IntegerField(null=True) 
   bookable = models.BooleanField(default=True)
   
   def __unicode__(self):
      return '<timeslot_id: %s, boat_id: %s' % (self.timeslot.id, self.boat.id)


 
# Booking model
class Booking(models.Model):
   timeslot = models.ForeignKey(Timeslot)
   boat     = models.ForeignKey(Boat)
   size     = models.IntegerField()
   
   def __unicode__(self):
     return '<timeslot_id: %s, boat_id: %s, size: %s>' % (self.timeslot.id, self.boat.id, self.size) 




