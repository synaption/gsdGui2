import datetime
import dateutil.parser

timestamp = '/home/ubuntu2004/impulses/raspberrypi-gsd-dev/timestamp'
onsettest = '/home/ubuntu2004/impulses/raspberrypi-gsd-dev/onsetstest'

def readfile(filename):
    f = open(filename, "r")
    text = f.read()
    f.close()
    return text

def readtoint(filename):
    return int(readfile(filename))

def readtime(filename):
    date_time_str = readfile(filename)
    date_time_str = date_time_str[:-4]
    date_time_obj = datetime.datetime.strptime(date_time_str, '%m_%d_%Y_%H_%M_%S_%f')
    print('Date:', date_time_obj.date())
    print('Time:', date_time_obj.time())
    return date_time_obj

def readoffset(timestamp, onsettest):
    date_time_str = addoffset(timestamp, onsettest)
    date_time_obj = datetime.datetime.strptime(date_time_str, '%S.%f')
    print('Time:', date_time_obj.time())
    return date_time_obj.time()

def addoffset(timestamp, onset):
    starttime = readtime(timestamp)
    offset = float(readfile(onset))
    delta = datetime.timedelta(seconds = offset)
    impulsetime = (starttime + delta)
    print (impulsetime)
    return impulsetime


def tdoa(first_time, later_time):
    x,y,td = str(later_time - first_time).split(":")
    #print(td)
    return float(td)


if __name__ == '__main__':
    first_time = readtime(timestamp)
    #later_time = addoffset(timestamp, onsettest)
    #print(tdoa(first_time, later_time))