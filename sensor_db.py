from time import sleep
from random import randint
from datetime import datetime as dt
from datetime import timedelta
import time
import subprocess
import math

class Db(object):

    conn = None;
    step = 30
    ISO_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
    filename = '/home/pi/projects/lilybot/hub/sensors.rrd'

    archive = [
            'DS:temp:GAUGE:30:0:100',
            'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
            'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
            'RRA:AVERAGE:0.5:10:1440',  # 10 minute averge for 7 days
            'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        ]

    # Archives hould be name with boit name in decimal form.
    bots = ['ardyh.bots.rpi1', 'ardyh.bots.rpi2', 'ardyh.bots.rpi3']
    grovebot_archive = [
        'DS:temp:GAUGE:30:0:100',
        'DS:humidity:GAUGE:30:0:100',
        'DS:light:GAUGE:30:0:1200',
        'DS:lux:GAUGE:30:0:1200',
        'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
        'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
        'RRA:AVERAGE:0.5:20:1440',  # 10 minute averge for 7 days
        'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        'RRA:AVERAGE:0.5:360:1480',  # 3 hrs averge for 185 days
    ]

    archive2 = [
        'DS:temp:GAUGE:30:0:100',
        'DS:humidity:GAUGE:30:0:100',
        'DS:light:GAUGE:30:0:1200',
        'DS:lux:GAUGE:30:0:1200',
        'RRA:AVERAGE:0.5:2:1440',  # 1 minute average for 24 hours
        'RRA:AVERAGE:0.5:10:1440',  # 5 minute averge for 3 days
        'RRA:AVERAGE:0.5:20:1440',  # 10 minute averge for 7 days
        'RRA:AVERAGE:0.5:60:1488',  # 30 minute averge for 31 days
        'RRA:AVERAGE:0.5:360:1480',  # 3 hrs averge for 185 days
        ]

    device_archive = [
        'DS:present:GAUGE:60:0:1',
        'RRA:AVERAGE:0.5:1:1440',  # 1 minute average for 24 hours
        'RRA:AVERAGE:0.5:5:1440',  # 5 minute averge for 3 days
        'RRA:AVERAGE:0.5:10:1440',  # 10 minute averge for 7 days
        'RRA:AVERAGE:0.5:30:1488',  # 30 minute averge for 31 days
        'RRA:AVERAGE:0.5:180:1480',  # 3 hrs averge for 185 days
    ]


    def __init__(self):
        self.create_bots()
        

    def create(self, filename=None, archive=None, step=None, no_overwrite=True):
        """

        rrdtool create target.rrd --start 1023654125 --step 300 DS:mem:GAUGE:600:0:671744 RRA:AVERAGE:0.5:12:24 RRA:AVERAGE:0.5:288:31
        

        """
        
        if not filename: filename = self.filename
        if not archive: archive = self.archive
        if not step: step = self.step
        
        cmd = "rrdtool create %s --step %s" %(filename, step)
        if no_overwrite:
            cmd = cmd + " --no-overwrite"
        cmd = cmd + ' ' + ' '.join(archive)
        print cmd
        subprocess.call(cmd, shell=True)


    def create_grovebot(self, bot):
        """
        Creates a new Grovebot archive. It will NOT overwrite an existing archive.

        Args:
            bot: [String] the unique name of the bot, e.g. "ardyh/bots/rpi2". This will
                 be used to create file for the db, the file name will replce the "/" with a "."

        Returns: None

        """
        self.create(self.get_filename(bot), self.grovebot_archive)


    def create_bots(self):
        for bot in self.bots:
            self.create(self.get_filename(bot), self.archive2)


    def _fetch(self, fname, start=None, end=None):
        """

        start and end should be datetime objects

        rrdtool fetch test.rrd AVERAGE --start 920804400 --end 920809200

        """


        cmd = "rrdtool fetch %s AVERAGE" %(fname)
        if start:
            cmd = cmd + ' --start %s' %(start)

        if end:
            cmd = cmd + ' --end %s' %(end)

        print cmd
        rs = subprocess.check_output(cmd, shell=True)
        return rs


    def update(self, bot, vals):
        """
        This should be renamed to the update_grovebot.
        Args:
            bot: [String] the unique name of the bot, e.g. "ardyh/bots/rpi2". This will
                 be used to create file for the db, the file name will replce the "/" with a "."

            vals: [Dict] Keyword: 'light', 'lux', 'timestamp', 'temp', 'humidity'

        rrdtool update target.rrd N:$total_mem
        
        """
        bot = bot.replace("/", ".")
        val = ":".join([str(v) for v in vals]).replace("None", "U")
        cmd = "rrdtool update %s N:%s" %(self.get_filename(bot), val)
        print cmd
        subprocess.call(cmd, shell=True)


    def fetch(self, bot=None, start=None, end=None):
        """

        This should be renamed to the update_grovebot.
        Args:
            bot: [String] the unique name of the bot, e.g. "ardyh/bots/rpi2". This will
                 be used to create file for the db, the file name will replce the "/" with a "."

            start: [Integer] Seconds since Unix Epoch (negative values are allowed)
            start: [Integer] Seconds since Unix Epoch (negative values are allowed)

        Example Command:
            rrdtool fetch test.rrd AVERAGE --start 920804400 --end 920809200

        """


        # cmd = "rrdtool fetch %s AVERAGE" %(self.get_filename(bot))
        # if start:
        #     cmd = cmd + ' --start %s' %(start)

        # if end:
        #     cmd = cmd + ' --end %s' %(end)

        # print cmd
        # rs = subprocess.check_output(cmd, shell=True)
        # # out  = [(int(item.split(": ")[0]), float(item.split(": ")[1])) 
        # #             for item in  rs.strip().split('\n')[3:] ]
        rs = self._fetch(self.get_filename(bot), start, end)
        out = []
        for row  in rs.strip().split('\n')[3:]:
            ts, vals = row.split(": ")
            ts_verbose = dt.fromtimestamp(int(ts)).strftime(self.ISO_FORMAT)
            new_row = [int(ts)]
            for val in vals.split(" "):
                if val == 'nan':
                    val = None
                else:
                    val = round(float(val), 2)
                new_row.append(val)

            out.append(new_row)


        print "%s entries, starting %s and on %s" %(len(out),out[0][2], out[-1][2])
        return out

    def create_device(self, mac):
        """
        This create a db for device logging by mac address.
        """
        fname = mac.replace(":","_") + ".rrd"
        self.create(fname, self.device_archive, 60, True)


    def update_device(self, mac, val):
        """
        This create a db for device logging by mac address.
        """
        fname = mac.replace(":","_") + ".rrd"
        cmd = "rrdtool update %s N:%s" %(fname, val)
        print cmd
        subprocess.call(cmd, shell=True)


    def fetch_device(self, mac, start=None, end=None):
        fname = "jobs/" + mac.replace(":","_") + ".rrd"
        rs = self._fetch(fname, start, end)
        out = []
        print rs
        for row  in rs.strip().split('\n')[3:]:
            ts, val = row.split(": ")
            ts_verbose = dt.fromtimestamp(int(ts)).strftime(self.ISO_FORMAT)
            if val == 'nan':
                val = 0
            out.append([int(ts), val])
        return out



    def utc(self, dt_obj):
        tt = dt.timetuple(dt_obj)
        return int(time.mktime(tt))

    def utc_now(self):
        now = dt.now()
        return self.utc(now)

    def get_filename(self, bot):
        return "%s.rrd" %(bot.replace("/", "."))

if __name__ == "__main__":
    db = Db()
    # db.create2()
    # db.update2(db.bots[1], [23, 75, 1000, 1200])
    # rs = db.fetch2(db.bots[1])
    # print rs

    # now = dt.now()
    # start = now - timedelta(minutes=30)
    # end = now - timedelta(minutes=0)
    # rs = db.fetch(start=start, end=end)
    # print rs
    # import pdb; pdb.set_trace()

    # while True:
    #     vals = [randint(10,50)]*4
    #     db.update2(db.bots[0], vals)
    #     db.update2(db.bots[1], vals)
    #     print "Added value %s" %vals
    #     sleep(5)



