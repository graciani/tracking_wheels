import hashlib

class event(object):
  '''Event defined by its json description.'''
  def __init__(self, json_description):
    self.event = json_description["event"]
    self.montecarlo = json_description["montecarlo"]
    self.number_of_sensors = self.event["number_of_sensors"]
    self.number_of_hits = self.event["number_of_hits"]
    self.hits = []
    for s in range(self.number_of_sensors):
      for i in range(self.event["sensor_hits_starting_index"][s], 
      self.event["sensor_hits_starting_index"][s] + self.event["sensor_number_of_hits"][s]):
        self.hits.append(hit(self.event["hit_x"][i], self.event["hit_y"][i], self.event["hit_z"][i],
        self.event["hit_id"][i], i, s))
    self.sensors = [
      sensor(s,
        self.event["sensor_module_z"][s],
        self.event["sensor_hits_starting_index"][s],
        self.event["sensor_number_of_hits"][s],
        self.hits
      ) for s in range(0, self.number_of_sensors)
    ]

  def copy(self):
    return event({"event": self.event, "montecarlo": self.montecarlo})

class track(object):
  '''A track, essentially a list of hits.'''
  def __init__(self, hits):
    self.hits = hits

  def add_hit(self, hit):
    self.hits.append(hit)

  def __repr__(self):
    return "Track hits #" + str(len(self.hits)) + ": " + str(self.hits)

  def __iter__(self):
    return iter(self.hits)

  def __eq__(self, other):
    return self.hits == other.hits

  def __ne__(self, other):
    return not self.__eq__(other)

  def __hash__(self):
      return int.from_bytes(hashlib.sha256(
        ''.join([str(h.id) for h in self.hits]).encode('utf-8')).digest(), byteorder='big')


class hit(object):
  '''A hit, composed of an id and its x, y and z coordinates.
  It may optionally contain the number of the sensor where
  the hit happened.
  '''
  def __init__(self, x, y, z, hit_id, hit_number=-1, sensor=-1):
    self.x = x
    self.y = y
    self.z = z
    self.id = hit_id
    self.hit_number = hit_number
    self.sensor_number = sensor

  def __getitem__(self, index):
    if (index<0 or index>2):
      raise IndexError

    if (index==0): return self.x
    elif(index==1): return self.y
    else: return self.z

  def __repr__(self):
    return "#" + str(self.hit_number) + " {" + str(self.x) + ", " + \
           str(self.y) + ", " + str(self.z) + "}"

  def __eq__(self, other):
      return self.id == other.id

  def __ne__(self, other):
      return not self.__eq__(other)

  def __hash__(self):
      return self.id


class sensor(object):
  '''A sensor is identified by its number.
  It also contains the z coordinate in which it sits, and
  the list of hits it holds.

  Note sensors are ordered by z, so the less the sensor_number,
  the less the z.
  '''
  def __init__(self, sensor_number, z, start_hit, number_of_hits, hits):
    self.sensor_number = sensor_number
    self.z = z
    self.hit_start_index = start_hit
    self.hit_end_index = start_hit + number_of_hits
    self.__global_hits = hits

  def __iter__(self):
    return iter(self.__global_hits[self.hit_start_index : self.hit_end_index])

  def __repr__(self):
    return "Sensor " + str(self.sensor_number) + ":\n" + \
      " At z: " + str(self.z) + "\n" + \
      " Number of hits: " + str(len(self.hits())) + "\n" + \
      " Hits (#id {x, y, z}): " + str(self.hits())

  def hits(self):
    return self.__global_hits[self.hit_start_index : self.hit_end_index]
