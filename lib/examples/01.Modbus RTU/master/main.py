import utime

while True:
  try:
    dt_tm=plc.modbus_master485.connection.read_input_registers(slave_addr=10, starting_addr=1, register_qty=2)
    date=utime.gmtime(int.from_bytes( bytes( [dt_tm[0].to_bytes(2,'big')[0], dt_tm[0].to_bytes(2,'big')[1], dt_tm[1].to_bytes(2,'big')[0], dt_tm[1].to_bytes(2,'big')[1]] ) ,'big'))
    date_str=str(date[0])+"-"+str('%0*d' % (2, date[1]))+"-"+str('%0*d' % (2, date[2]))+" "+str('%0*d' % (2, date[3]))+":"+str('%0*d' % (2, date[4]))+":"+str('%0*d' % (2, date[5]))
    free_ram=plc.modbus_master485.connection.read_input_registers(slave_addr=10, starting_addr=3, register_qty=1)[0]/100
    free_vfs=plc.modbus_master485.connection.read_input_registers(slave_addr=10, starting_addr=4, register_qty=1)[0]/100
    
    print("Remote time: {0}, free RAM: {1}%, free VFS: {2}%".format(date_str,free_ram,free_vfs))
    utime.sleep(10)
    
  except KeyboardInterrupt:
    print('KeyboardInterrupt, stopping RTU master...')
    break
  except Exception as e:
    print('Exception during execution: {}'.format(e))