'''
This module is for demultiplexing of data from any Illumina based machine using BCL2FASTQ
As part of the overall Plug and Play Bioinformatics GUI

Written by TicklishGiraffe
'''
import tkinter, os, sys, subprocess, shutil, logging, datetime, time
from tkinter import filedialog as fd
from subprocess import Popen, PIPE

currentmonth=datetime.datetime.now().strftime('%m')
currentday=datetime.datetime.now().strftime('%d')
currentyear=datetime.datetime.now().strftime('%Y')
logname='demultiplexing_log_started_on_'+currentmonth+'_'+currentday+'_'+currentyear
logger=logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler=logging.FileHandler(logname)
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

#Check is BLC2fastq is there, try to install if not
try:
    bcl=subprocess.call('bcl2fastq -v', shell=True)
    if bcl==0:
        logger.info('BCL2Fastq is currently on this machine')
    else:
        logger.info('BCL2Fastq is not on this machine, attempting to add it...')
        import BCL2FASTQINSTALL
        bcl2=subprocess.call('bcl2fastq -v', shell=True)
        if bcl2==0:
            logger.info('BCL2Fastq successfully installed')
        else:
            logger.info('BCL2Fastq has failed to install. Please check install log and manually install')
            error=tkinter.Tk()
            errorlabel=tkinter.Label(error, text='Error has arrisen, please see log')
            errorbutton=tkinter.Button(error, text='Exit', command=error.destroy)
            errorlabel.pack()
            errorbutton.pack()
            error.mainloop()
            exit()
                  
except:
    logger.info('Cannot communicate with the system?')
    error=tkinter.Tk()
    errorlabel=tkinter.Label(error, text='Error has arrisen, please see log')
    errorbutton=tkinter.Button(error, text='Exit', command=error.destroy)
    errorlabel.pack()
    errorbutton.pack()
    error.mainloop()
    exit()
    
#gui set up
demulti=tkinter.Tk()
demulti.config(background='deep sky blue')
demulti.title('Demultiplexing with GUI')

startmessage=tkinter.Message(demulti, width=700, background='deep sky blue', font=('Helvetica',16), text='''
Welcome to this beautiful version of demultiplexing!
To perform demultiplexing, use the buttons below to find their stated target.

While searching for the "Run Folder", please select the folder that is the entire sequencing run
IE: 160215_NB500952_0043_AHYFMGBGXX

While searching for the "Sample Sheet", please make sure you select the appropriate sample sheet for the run.
Failure to do so will cause the demultiplexing to fail

Once you select both the Run Folder and Sample Sheet, the final button will become active and allow you to begin demultiplexing.
DO NOT EXIT WHILE IT IS RUNNING!
It will just cause you problems.

Average run time for NextSeq Mid run will be ~30 minutes, for High will be ~60-90 minutes.

''')
startmessage.pack()

folderclick=False
sampleclick=False

def clickcheck():
    if folderclick==True and sampleclick==True:
        runbutton.config(state='active')
    else:
        pass

def runfolder():
    global folder
    folder=fd.askdirectory()
    runfolderbutton.config(state='disabled')
    global folderclick
    folderclick=True
    clickcheck()
    logging.info('Run folder is '+folder)
    return folder
    
    

def samplesheet():
    global ss
    ss=fd.askopenfilename()
    samplesheetbutton.config(state='disabled')
    global sampleclick
    sampleclick=True
    clickcheck()
    logging.info('Sample sheet is '+ss)
    return ss

def go():
    try:
        os.system("bcl2fastq --runfolder-dir "+folder+" --output-dir "+folder+"/manualFASTQS --sample-sheet "+ss+" --no-lane-splitting")
    except:
        errorpop=tkinter.Toplevel(bg="firebrick3")
        errorpop.title('ERROR')
        errormes=tkinter.Message(errorpop, background='firebrick3',font=('Helvetica', 20), text="ERROR! An error has occured during your demultiplexing.  Find an administrator to fix it.")
        errormes.pack()
        exitbut=tkinter.Button(errorpop, text='Exit', command=demulti.destroy)
        exitbut.pack()

    if os.path.exists(folder+"/manualFASTQS/Reports"):
        shutil.copy(ss, folder+"/sample_sheet.csv")
        exitbutton=tkinter.Button(demulti,font=('Helvetica',14), text='Congratulations! Your demultiplexing is completed! Please click on this button to exit the program.  Enjoy your data!', command=demulti.destroy)
        exitbutton.pack()
        startmessage.pack_forget()
        runfolderbutton.pack_forget()
        samplesheetbutton.pack_forget()
        runbutton.pack_forget()
        
    else:
        errorbutton=tkinter.Button(demulti,font=('Helvetica', 14), background="firebrick3", text="Uh oh! ERROR! An error has occured during your demultiplexing.  Find an administrator to fix it.", command=demulti.destroy)
        errorbutton.pack()
        startmessage.pack_forget()
        runfolderbutton.pack_forget()
        samplesheetbutton.pack_forget()
        runbutton.pack_forget()
        
        
runfolderbutton=tkinter.Button(demulti, width=50, font=('Helvetica',14),text='Click here for Run Folder', command=runfolder)
samplesheetbutton=tkinter.Button(demulti, width=50, font=('Helvetica',14),text='Click here for Sample Sheet', command=samplesheet)
runfolderbutton.pack()
samplesheetbutton.pack()

runbutton=tkinter.Button(demulti, width=50, font=('Helvetica',14), text='Click here once input is complete to start Demultiplexing!', command=go)
runbutton.config(state='disabled')
runbutton.pack()

exitbutton=tkinter.Button(demulti, width=50, font=('Helvetica', 14), text='Exit', command=demulti.destroy)
exitbutton.pack()

demulti.mainloop()


