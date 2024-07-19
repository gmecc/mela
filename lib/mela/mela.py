import gc
import os
#======================================================================================================




#--------------------------------------------------------------------
#
#   Main class for our board
#
#--------------------------------------------------------------------
class Mela:
  def __init__(self):
    self.info=Mela_info()

#--------------------------------------------------------------------
#
#    Information class for our board
#
#--------------------------------------------------------------------
class Mela_info:
  def __init__(self):
    if not gc.isenabled(): gc.enable()
    gc.collect()

  @property
  def df(self):
    s = os.statvfs('//')
    T=(s[1]*s[2])/1048576
    F=(s[0]*s[3])/1048576
    P = '{0:.2f}%'.format(F/T*100)
    return ('VFS: Total:{0} Mb Free:{1} Mb ({2})'.format(T,F,P))

  @property
  def free(self):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    return ('RAM: Total:{0} bytes Free:{1} bytes ({2})'.format(T,F,P))
