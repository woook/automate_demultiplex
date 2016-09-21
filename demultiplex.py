'''
Created on 19 Sep 2016

This script loops through all the run folders in a directory looking for any newly completed runs ready to be demultiplexed
The run is deemed complete by the presense of a files called RTAComplete.txt. This will only be created when the run is ready for demultiplexing.
A sample sheet must be present so a samplesheet with the name of the run_samplesheet.csv must be present in the samplesheets folder.
Finally a check that the demultiplexing has (or is) not already being performed.

If the run is ready for demultiplexing then a command is issued.
The stdout and stderr is written to a log file (the same file which is checked for above).

Could possibly add a check/message if it fails.
 
@author: aled
'''

import os
import subprocess


class get_list_of_runs():
    '''Loop through the directories in the directory containing the runfolders'''
    def __init__(self):
        # directory of run folders - must be same as in ready2start_demultiplexing()
        self.runfolders = "/home/aled/demultiplex_testing"

    def loop_through_runs(self):
        # create a list of all the folders in the runfolders directory
        all_runfolders = os.listdir(self.runfolders)
        # for each folder if it is not samplesheets pass the runfolder to the next class ready2start_demultiplexing()
        for folder in all_runfolders:
            if folder != "samplesheets":
                ready2start_demultiplexing().has_run_finished(folder)


class ready2start_demultiplexing():
    '''This class checks if a run is ready to be demultiplexed (samplesheet present, run finished and not previously demultiplexed) and if so runs demultiplexes''' 
    def __init__(self):
        # directory of run folders - must be same as in get_list_of_runs()
        self.runfolders = "/home/aled/demultiplex_testing"
        #set the samplesheet folders
        self.samplesheets = self.runfolders + "/samplesheets"
        # file which denotes end of a run
        self.complete_run = "RTAComplete.txt"
        # file which denotes demultiplexing is underway/complete 
        self.demultiplexed = "demultiplexlog.txt"
        # set empty variables to be defined based on the run  
        self.runfolder = ""
        self.runfolderpath = ""
        self.samplesheet = ""
        # path to bcl2fastq
        self.bcl2fastq = "/usr/local/bcl2fastq2-v2.17.1.14/bin/bcl2fastq"
        #succesful run
        self.logfile_success="Processing completed with 0 errors and 0 warnings."
        

    def has_run_finished(self, runfolder):
        ''' check for presence of RTAComplete.txt to denote a finished sequencing run'''
        # capture the runfolder 
        self.runfolder = str(runfolder)
        print "reading " + self.runfolder
        
        # create full path to runfolder
        self.runfolderpath = self.runfolders + "/" + self.runfolder
        # check if the RTAcomplete.txt file is present
        if os.path.isfile(self.runfolderpath + "/" + self.complete_run):
            print "runcomplete"
            #if so proceed
            self.already_demultiplexed()
        else:
            # else stop 
            print "run not complete"

    def already_demultiplexed(self):
        '''check if the runfolder has been demultiplexed (demultiplex_log is present)'''
        # if the log file is present
        if os.path.isfile(self.runfolderpath + "/" + self.demultiplexed):
            # stop
            print "has been demultiplexed"
        else:
            print "not demultiplexed yet"
            # else proceed
            self.look_for_sample_sheet()

    def look_for_sample_sheet(self):
        '''check sample sheet is present'''
        # set name and path of sample sheet to find
        self.samplesheet=self.samplesheets + "/" + self.runfolder + "_SampleSheet.csv"
        # if the samplesheet is present 
        if os.path.isfile(self.samplesheet):
            print "samplesheet present"
            # proceed
            self.run_demuliplexing()
        else:
            # stop
            print "no samplesheet"

    def run_demuliplexing(self):
        '''Run the demultiplexing'''
        
        print "demultiplexing...."+self.runfolder
        # example command sudo /usr/local/bcl2fastq2-v2.17.1.14/bin/bcl2fastq -R /media/data1/share/160914_NB551068_0007_AHGT7FBGXY --sample-sheet /media/data1/share/samplesheets/160822_NB551068_0006_AHGYM7BGXY_SampleSheet.csv --no-lane-splitting
        
        # practice command: 
        # command = "fv samtools faidx /home/aled/Documents/Reference_Genomes/hg19.fa xfvg chr1:10000000-10000002"
        
        # create the command
        command = self.bcl2fastq + " -R " + self.runfolders+"/"+self.runfolder + " --sample-sheet " + self.samplesheet + " --no-lane-splitting"
        # command="/usr/local/bcl2fastq2-v2.17.1.14/bin/bcl2fastq -R 160822_NB551068_0006_AHGYM7BGXY/ --sample-sheet samplesheets/160822_NB551068_0006_AHGYM7BGXY_SampleSheet.csv --no-lane-splitting"
        
        # print command
        
        # open a log file
        demultiplex_log = open(self.runfolders+"/"+self.runfolder+"/"+self.demultiplexed,'w')
        
        # run the command, redirecting stderror to stdout
        proc = subprocess.Popen([command], stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
        
        # capture the streams (err is redirected to out above)
        (out, err) = proc.communicate()
        
        # write this to the log file
        demultiplex_log.write(out)
        # close log file
        demultiplex_log.close()
        
        # call_log_file_check
        self.check_demultiplexlog_file()
        
    def check_demultiplexlog_file(self):
        #open log file
        logfile=open(self.runfolders+"/"+self.runfolder+"/"+self.demultiplexed,'r')
        #print len(logfile)
        num_lines = sum(1 for line in logfile)
        
        last5rows=num_lines - 10
        print last5rows
        for linenumber, line in enumerate(logfile):
            if linenumber > last5rows:
                print linenumber
                print line
            
            
        
if __name__ == '__main__':
    # Create instance of get_list_of_runs
    runs = get_list_of_runs()
    # call function
    runs.loop_through_runs()
