import optparse
import sys

import matplotlib
matplotlib.use('Agg')
from pylab import *

# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self,file):
        """ Initialize plotter with a file name. """
        self.file = file
        self.loads = []
        self.delays = []
        self.model_times = [1, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95]
        self.model_delays = [.00000505, .0000556, .000125, .000214, .000333, \
			.0005, .00075, .001167, .002, .0045, .0095]
        self.runs = 0
    
    def multi_boxplot(self):
        clf()
        for n in range(0, self.runs):
		print('' + str(self.loads[n]) + ' mean: ' + \
			str(sum(self.delays[n]) / float(len(self.delays[n]))) + \
			', max: ' + str(max(self.delays[n])))
		boxplot(self.delays[n],positions=[self.loads[n]],widths=[2])
        plot(self.model_times, self.model_delays, c=cm.summer(0), label='theoretical')
        xlabel('Utilization (' + unichr(0x03c1) +')')
        ylabel('Queuing Delay (sec)')
        #yticks(range(0,1500,120))
        xticks(range(0,120,10))
        savefig('multi_box.png')

    def parse(self):
        cur_load = -1
        f = open(self.file)
        for line in f.readlines():
            if line.startswith("#"):
                continue
            try:
                util,tx_delay,prop_delay,q_delay = line.split()
                #t,download,size = line.split()
            except:
                continue
            util = float(util) * 100
            q_delay = float(q_delay)
            if cur_load != util:
                cur_load = util
                self.runs += 1
                self.loads.append(util)
                self.delays.append([])
                
            self.delays[self.runs - 1].append(q_delay)
    
    

def parse_options():
	# parse options
	parser = optparse.OptionParser(usage = "%prog [options]",
								   version = "%prog 0.1")

	parser.add_option("-f","--file",type="string",dest="file",
					  default=None,
					  help="file")

	(options,args) = parser.parse_args()
	return (options,args)


if __name__ == '__main__':
    (options,args) = parse_options()
    if options.file == None:
        print "plot.py -f file"
        sys.exit()
    p = Plotter(options.file)
    p.parse()
    p.multi_boxplot()
