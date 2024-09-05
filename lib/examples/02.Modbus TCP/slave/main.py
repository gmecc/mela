from machine import Timer

timer_0 = Timer(0) # Between 0-3 for ESP32

def interruption_handler(timer):
  tmp_time=plc.rtc.now_em_unixtime.to_bytes(4,'big')
  bytes_timestamp=(int.from_bytes(bytes([tmp_time[0], tmp_time[1]]),'big'),int.from_bytes(bytes([tmp_time[2], tmp_time[3]]),'big'))
  plc.modbus_slaveTCP.connection.set_ireg(1,bytes_timestamp)
  plc.modbus_slaveTCP.connection.set_ireg(3,int(float(plc.info.free(False))*100))
  plc.modbus_slaveTCP.connection.set_ireg(4,int(float(plc.info.df(False))*100))

timer_0.init(mode=Timer.PERIODIC, period=1000, callback=interruption_handler)

while True:
    try:
        result = plc.modbus_slaveTCP.connection.process()
        if result:
          print("Response sent.")
    except KeyboardInterrupt:
        print('KeyboardInterrupt, stopping TCP client...')
        break
    except Exception as e:
        print('Exception during execution: {}'.format(e))
