def traceproc(aerolevel,aerofilt_dir):
    import hysplit_tools as tools
    import os, sys
    import scipy.io
    import numpy as np

    startdir = os.getcwd()

    topdir = aerofilt_dir+'\Level '+aerolevel

    os.chdir(topdir)

    data_files = os.listdir(os.getcwd())

    d_mean = []
    d_std = []
    t_mean = []
    t_std = []
    endpos_mean = []
    endpos_std = []
    start_time = []
    station = []

    #run through all location folders
    for f in data_files:
        if os.path.isdir(f):
            os.chdir(f)
            tracefile = f+'traceback2'
            #open traceback file
            tracedict = scipy.io.loadmat(tracefile)

            #create a separate dict of lists for each day and put those into a
            #list called dictlist

            dates = tracedict['start_date']
            keys = tracedict.keys()

            oldday = dates[0][2]

            tempdict = dict()
            dictlist = []

            #ignore these keys that come attached to the dictionary from loadmat
            rejectlist = ['__globals__','__header__','__version__']

            for k,v in tracedict.iteritems():
                if k not in rejectlist:
                    tempdict[k] = []
                    tempdict[k].append(v[0])

            for n in range(1,len(dates)):
                newday = dates[n][2]
                if newday == oldday:
                    for k,v in tracedict.iteritems():
                        if k not in rejectlist:
                            tempdict[k].append(v[n])
                    oldday = newday
                else:
                    dictlist.append(tempdict)
                    tempdict = dict()
                    for k,v in tracedict.iteritems():
                        if k not in rejectlist:
                            tempdict[k] = []
                            tempdict[k].append(v[n])               
                    oldday = newday

            dictlist.append(tempdict)
            
            #generate mean daily values for each element of the dictionaires
            
            for line in dictlist:
                d_mean.append(np.mean(line['delta_d']))
                d_std.append(np.std(line['delta_d']))
                t_mean.append(np.mean(line['delta_t']))
                t_std.append(np.std(line['delta_t']))

                endpos_mean.append(np.mean(line['end_loc'],axis=0))
                endpos_std.append(np.std(line['end_loc'],axis=0))
                start_time.append(line['start_date'][0])
                station.append(str(line['station'][0]))

            os.chdir('..')

    output_dict = {'d_mean':d_mean,'d_std':d_std,'t_mean':t_mean,'t_std':t_std,\
                   'endpos_mean':endpos_mean,'endpos_std':endpos_std,\
                   'start_time':start_time,'station':station}

    scipy.io.savemat('Hyproc'+aerolevel,output_dict)

    os.chdir(startdir)

    
def aeroproc(aerolevel,aerofilt_dir):
    import hysplit_tools as tools
    import os, sys
    import scipy.io
    import numpy as np

    startdir = os.getcwd()

    topdir = aerofilt_dir+'\Level '+aerolevel

    os.chdir(topdir)

    data_files = os.listdir(os.getcwd())

    total_mean = []
    total_std = []
    fine_mean = []
    fine_std = []
    coarse_mean = []
    coarse_std = []
    inpoint = []
    numdist_mean = []
    numdist_std = []
    station = []
    date = []
    diameters = []

    #run through all location folders
    for f in data_files:
        if os.path.isdir(f):
            os.chdir(f)
            aerofile = 'Aerostats_'+f+'_'+aerolevel
            #open traceback file
            aerodict = scipy.io.loadmat(aerofile)

            #create a separate dict of lists for each day and put those into a
            #list called dictlist

            dates = aerodict['Date']
            keys = aerodict.keys()

            oldday = dates[0][-2]

            tempdict = dict()
            dictlist = []

            #ignore these keys that come attached to the dictionary from loadmat
            rejectlist = ['__globals__','__header__','__version__']

            for k,v in aerodict.iteritems():
                if k == 'Diameters':
                    tempdict[k] = []
                    tempdict[k].append(v)
                elif k == 'Numdist':
                    tempdict[k] = []
                    tempdict[k].append(v[:,0])
                elif k not in rejectlist:
                    tempdict[k] = []
                    tempdict[k].append(v[0])  

            for n in range(1,len(dates)):
                newday = dates[n][-2]
                if newday == oldday:
                    for k,v in aerodict.iteritems():
                        if k == 'Diameters':
                            tempdict[k].append(v)
                        elif k == 'Numdist':
                            tempdict[k].append(v[:,n])
                        elif k not in rejectlist:
                            tempdict[k].append(v[n])
                    oldday = newday
                else:
                    dictlist.append(tempdict)
                    tempdict = dict()
                    for k,v in aerodict.iteritems():
                        if k == 'Diameters':
                            tempdict[k] = []
                            tempdict[k].append(v)
                        elif k == 'Numdist':
                            tempdict[k] = []
                            tempdict[k].append(v[:,n])
                        elif k not in rejectlist:
                            tempdict[k] = []
                            tempdict[k].append(v[n])            
                    oldday = newday

            dictlist.append(tempdict)        
            #generate mean daily values for each element of the dictionaires
            
            for line in dictlist:
                total_mean.append([np.mean(line['EffRad-T']),np.mean(line['VolMedianRad-T']),\
                               np.mean(line['VolCon-T']),np.mean(line['StdDev-T'])])
                total_std.append([np.std(line['EffRad-T']),np.std(line['VolMedianRad-T']),
                               np.std(line['VolCon-T']),np.std(line['StdDev-T'])])
                
                fine_mean.append([np.mean(line['EffRad-F']),np.mean(line['VolMedianRad-F']),
                               np.mean(line['VolCon-F']),np.mean(line['StdDev-F'])])
                fine_std.append([np.std(line['EffRad-F']),np.std(line['VolMedianRad-F']),
                               np.std(line['VolCon-F']),np.std(line['StdDev-F'])])

                coarse_mean.append([np.mean(line['EffRad-C']),np.mean(line['VolMedianRad-C']),
                               np.mean(line['VolCon-C']),np.mean(line['StdDev-C'])])
                coarse_std.append([np.std(line['EffRad-C']),np.std(line['VolMedianRad-C']),
                               np.std(line['VolCon-C']),np.std(line['StdDev-C'])])         

                inpoint.append(np.mean(line['Inflection_Point[um]']))

                numdist_mean.append(np.mean(line['Numdist'],axis=0))
                numdist_std.append(np.std(line['Numdist'],axis=0))

                station.append(f)

                date.append(np.mean(line['Date'],axis=0))

                diameters.append(line['Diameters'])
                
            os.chdir('..')

    output_dict = {'station':station,'date':date,'numdist_mean':numdist_mean,'numdist_std':numdist_std,\
                   'total_mean':total_mean,'total_std':total_std,'fine_mean':fine_mean,'fine_std':fine_std,\
                   'coarse_mean':coarse_mean,'coarse_std':coarse_std,'inpoint':inpoint,'diameters':diameters}

    scipy.io.savemat('Aeroproc'+aerolevel,output_dict)
            
    os.chdir(startdir)            
                                
                

def combproc(level,aerofilt_dir):
    import hysplit_tools as tools
    import os, sys
    import numpy as np
    import scipy.io

    startdir = os.getcwd()
    
    topdir = aerofilt_dir+'\Level '+aerolevel

    os.chdir(topdir)

    aerofile = 'Aeroproc'+aerolevel
    hyfile = 'Hyproc2'+aerolevel

    aerodict = scipy.io.loadmat(aerofile)
    hydict = scipy.io.loadmat(hyfile)

    #divide both dicts up by station

    aerostations = set(aerodict['station'])
    hystations = set(hydict['station'])

    #ignore these keys that come attached to the dictionary from loadmat
    rejectlist = ['__globals__','__header__','__version__']


    hylist = []
    for stat in hystations:
        tempdict = dict()
        for n in range(0,len(hydict['station'])):
            if hydict['station'][n] == stat:
                for key in hydict.keys():
                    if key not in rejectlist:
                        if key == 'start_time':
                            tempval = np.reshape(hydict[key][n],[1,4])
                        elif key == 'station':
                            tempval = [hydict[key][n]]
                        else:
                            tempval = hydict[key][n]

                        try:
                            tempdict[key].append(tempval)
                        except KeyError:
                            tempdict[key] = np.array(tempval)
                        except AttributeError:
                            tempdict[key] = np.vstack((tempdict[key],tempval))
        if len(tempdict['station']) != 1:
            hylist.append(tempdict)

    aerolist = []
    for stat in aerostations:
        tempdict = dict()
        for n in range(0,len(aerodict['station'])):
            if aerodict['station'][n] == stat:
                for key in aerodict.keys():
                    if key not in rejectlist:
                        if key == 'start_time':
                            tempval = [np.reshape(aerodict[key][n],[1,4])]
                        elif key == 'station':
                            tempval = [aerodict[key][n]]
                        else:
                            tempval = aerodict[key][n]
                        
                        try:
                            tempdict[key].append(tempval)
                        except KeyError:
                            tempdict[key] = np.array(tempval)
                        except AttributeError:
                            tempdict[key] = np.vstack((tempdict[key],tempval))
        if len(tempdict['station']) != 1:
            aerolist.append(tempdict)
    #remove dates where hysplit didn't find traces to deserts

    aerolist_mod = []
    for h in hylist:
        hydates = h['start_time'][:,2]
        hystation = h['station'][0]
        for a in aerolist:
            aerostation = a['station'][0]
            if aerostation == hystation:
                tempdict = dict()
                for n in range(0,len(a['station'])):
                    aerodate = a['date'][n,2]
                    if aerodate in hydates:
                        for key in a.keys():
                            try:
                                tempdict[key].append(a[key][n])
                            except KeyError:
                                tempdict[key] = a[key][n]
                            except AttributeError:
                                tempdict[key] = np.vstack((tempdict[key],a[key][n]))
                aerolist_mod.append(tempdict)

    output_dict = {'Hysplit':hylist,'Aeronet':aerolist_mod}

    scipy.io.savemat('Combproc2'+aerolevel,output_dict)
