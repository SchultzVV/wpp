import urllib.request;
import datetime;
import time
import pickle;import sys as s;import urllib;

#-----------------------------Here The Tools------------------------------------
def Style(which):
    if which==0:
        sources=['GEOCOLOR','AirMass','GEOCOLOR','Sandwich','GEOCOLOR','DayCloudPhase','GEOCOLOR','02','GEOCOLOR',\
        '04','GEOCOLOR','06','GEOCOLOR','07','GEOCOLOR','08','GEOCOLOR','09','GEOCOLOR','10','GEOCOLOR',\
        '11','GEOCOLOR','12','GEOCOLOR','15']
    if which==1:
        sources=['GEOCOLOR','AirMass','Sandwich','DayCloudPhase','02','04','06','07','08','09','10','11','12','15']
    if which==2:
        sources=['GEOCOLOR','AirMass','GEOCOLOR','Sandwich','GEOCOLOR','DayCloudPhase','GEOCOLOR','07','GEOCOLOR',\
        '10','GEOCOLOR','11','GEOCOLOR','15']
    if which==3:
        sources=['AirMass','Sandwich','DayCloudPhase','02','04','06','07','08','09','10','11','12','15']
    return sources
#-------------------------------------------------------------------------------
def fix(hour,minutes,TtoRemov):
    a=int(minutes)-TtoRemov
    hour,minutes=int(hour),int(minutes)
    #print(int(TtoRemov/60))
    if a<0:
        if hour==0:
            hour=23
        else:
            hour-=1
        minutes=60+a
    else:
        minutes=minutes-TtoRemov
    if minutes<10:
        minutes=str(minutes)
        minutes='0'+minutes
    if hour<10:
        hour=str(hour)
        hour='0'+hour
    return str(hour),str(minutes)
#-------------------------------------------------------------------------------
def timer_roulete(year,dayJ,hour,minute):
    y = str(year)
    if int(dayJ)<100:
        d = str(dayJ)
    else:
        d=str(dayJ)
    if int(dayJ)<10:
        d = '00'+str(dayJ)
    #if int(hour)<10:
    #    h = '0'+str(hour)
    #else:
    h=str(hour)
    m=str(minute)
    return str(y+d+h+m)
#-------------------------------------------------------------------------------
def url_source_resolution(time,source,resolution):
    if source == 'GEOCOLOR':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/GEOCOLOR/'
        url = urli+time+'_GOES16-ABI-FD-GEOCOLOR-'+resolution#'5424x5424.jpg'
        return url
    if source =='AirMass':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'AirMass/'+time+'_GOES16-ABI-FD-AirMass-'+resolution
        return url
    if source == 'Sandwich':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'Sandwich/'+time+'_GOES16-ABI-FD-Sandwich-'+resolution
        return url
    if source=='DayCloudPhase':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'DayCloudPhase/'+time+'_GOES16-ABI-FD-DayCloudPhase-'+resolution
        return url
    if source=='02':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'02/'+time+'_GOES16-ABI-FD-02-'+resolution
        return url
    if source=='04':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'04/'+time+'_GOES16-ABI-FD-04-'+resolution
        return url
    if source=='06':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'06/'+time+'_GOES16-ABI-FD-06-'+resolution
        return url
    if source=='07':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'07/'+time+'_GOES16-ABI-FD-07-'+resolution
        return url
    if source=='08':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'08/'+time+'_GOES16-ABI-FD-08-'+resolution
        return url
    if source=='09':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'09/'+time+'_GOES16-ABI-FD-09-'+resolution
        return url
    if source=='10':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'10/'+time+'_GOES16-ABI-FD-10-'+resolution
        return url
    if source=='11':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'11/'+time+'_GOES16-ABI-FD-11-'+resolution
        return url
    if source=='12':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'12/'+time+'_GOES16-ABI-FD-12-'+resolution
        return url
    if source=='13':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'13/'+time+'_GOES16-ABI-FD-13-'+resolution
        return url
    if source=='14':

        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'14/'+time+'_GOES16-ABI-FD-14-'+resolution
        return url
    if source=='15':
        urli='https://cdn.star.nesdis.noaa.gov/GOES16/ABI/FD/'
        url=urli+'15/'+time+'_GOES16-ABI-FD-15-'+resolution
        return url
#-------------------------------------------------------------------------------
def Instant_band_roulete(sources,resolution):
    aux = datetime.datetime.utcnow()
    day_of_year=aux.strftime('%j')
    time=str(aux)
    year = time[0:4]
    hour = time[11:13]
    minutes = time[14:16]
    minutes = minutes[:-1]+'0'
    hour,minutes=fix(hour,minutes,30)
    instant=timer_roulete(year,day_of_year,hour,minutes)
    try:
        last_index = pickle.load( open( "L_I", "rb" ) )
    except:
        last_index = 0
    if last_index==0:
        index = 0
        source=sources[index]
        index+= 1
#    if last_index>len(sources)-1:
#        index = 0
#        source=sources[index]
    if last_index==len(sources)-1:
        index = 0
        source=sources[index]
    else:
        index = last_index+1
#        print(index)
        source=sources[index]
    print(index)
    print(last_index)
    print(len(sources)-1)
    url=url_source_resolution(instant,source,resolution)
    address = open("L_I","wb")
    pickle.dump(index, address)
    address.close()
    try:
        urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
    except:
        pass
#-------------------------------------------------------------------------------
def Instant_Geocolor(resolution):
    aux = datetime.datetime.utcnow()
    day_of_year=aux.strftime('%j')
    time=str(aux)
    year = time[0:4]
    hour = time[11:13]
    minutes = time[14:16]
    minutes = minutes[:-1]+'0'
    hour,minutes=fix(hour,minutes,30)
    instant=timer_roulete(year,day_of_year,hour,minutes)
    #url=url_source(instant,'GEOCOLOR')
    url=url_source_resolution(instant,'GEOCOLOR',resolution)
    #url=Resolution_change(url,resolution)
    try:
        urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
    except:
        pass
#------------------------------------------------------------------------------
def Instant_source(source,resolution):
    aux = datetime.datetime.utcnow()
    day_of_year=aux.strftime('%j')
    print(day_of_year)
    time=str(aux)
    year = time[0:4]
    print(year)
    hour = time[11:13]
    minutes = time[14:16]
    minutes = minutes[:-1]+'0'
    hour,minutes=fix(hour,minutes,50)
    instant=timer_roulete(year,day_of_year,hour,minutes)
    #url=url_source(instant,'GEOCOLOR')
    url=url_source_resolution(instant,source,resolution)
    #url=Resolution_change(url,resolution)
    print(url)
    urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
    try:
        urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
    except:
        print('nao tem data')
        pass
#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------
def Days_evolution_band_roulete(Year,Di,Df,Hi,Hf,Mi,Mf,source,resolution):
    for dayJ in range(Di,Df):
        for hora in range(Hi,Hf):
            for minuto in range(Mi,Mf,10):
                instant=timer_roulete(Year,dayJ,hora,minuto)
                url=url_source_resolution(instant,source,resolution)
                print(url)
                try:
                    urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
                except:
                    pass
#-------------------------------------------------------------------------------
#------------------ Here Start the set of Wallpapers----------------------------
#-------------------------------------------------------------------------------
#------------------ Just ilumination, sun, moon---------------------------------
def get_sun_moon_wpp():
    aux = datetime.datetime.utcnow()
    time=str(aux)
    urli='https://www.timeanddate.com/scripts/sunmap.php?iso='
    year = time[0:4]
    month =time[5:7]
    day = time[8:10]
    hour = time[11:13]
    minutes = time[14:16]
    url = urli+year+month+day+'T'+hour+minutes+'&earth=1'
    urllib.request.urlretrieve(url,'bc (3rd copy).jpg')
    #return url
#get_sun_moon_wpp()
#s.exit()
#------------Image from Goes16, filters and real colors-------------------------
#------------Letícia's set -----------------------------------------------------
def Roulete():
    for i in Style(3):
        Instant_source(i,'1808x1808.jpg')
        #Instant_source(i,'678x678.jpg')
#Roulete()
#s.exit()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++AQQQQUIIII+++++++++++++++++++++++++++++++++++++++++
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Instant_band_roulete(Style(1),'1808x1808.jpg')
#Instant_band_roulete(Style(1),'678x678.jpg')
#s.exit()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 #-------------------------------------------------------------------------------
def Filters_endsGeocolor(sources):
    for i in sources:
        Instant_band_roulete(sources,'678x678.jpg')
    Instant_Geocolor('1808x1808.jpg')
#Filters_endsGeocolor(Style(3))
#s.exit()
#------------All the goes16 Data that remains in the website--------------------
def the_last_images(range,sources):
    aux = datetime.datetime.utcnow()
    time=str(aux)
    year = time[0:4]
    dayJ=aux.strftime('%j')
    dayF,dayI=int(dayJ),int(dayJ)-range
    hour = time[11:13]
    minutes = time[14:16]
    minutes = minutes[:-1]+'0'
    hour,minutes=fix(hour,minutes,30)
    print(year,dayI,dayF,'ae')
    for i in sources:
        Days_evolution_band_roulete(year,dayI,dayF,1,23,30,40,i,'678x678.jpg')
#range_of_days=1
#the_last_images(range_of_days,Style(3))
#s.exit()
#-------------------------------------------------------------------------------
'''     SE QUISER UM FILTRO ESPECÍFICO SÓ ESCOLHE ALGUM NESSA LINHA DE BAIXO'''
#sources=['GEOCOLOR','AirMass','Sandwich','DayCloudPhase','02','04','06','07','08','09','10','11','12','15']
'''     E POEM NESSA OUTRA LINHA AQUI, ESCOLHENDO A RESOLUÇÃO TAMBÉM
        como eu já fiz, é só descomentar o filtro que tu quer.
'''
Instant_source('AirMass','1808x1808.jpg')
Instant_source('Sandwich','1808x1808.jpg')
Instant_source('DayCloudPhase','1808x1808.jpg')
Instant_source('02','1808x1808.jpg')# B W
Instant_source('04','1808x1808.jpg')# B W
Instant_source('06','1808x1808.jpg')# B W
Instant_source('07','1808x1808.jpg')
Instant_source('08','1808x1808.jpg')
Instant_source('09','1808x1808.jpg')
Instant_source('10','1808x1808.jpg')
Instant_source('11','1808x1808.jpg')
Instant_source('12','1808x1808.jpg')
Instant_source('15','1808x1808.jpg')
#Instant_source('GEOCOLOR','1808x1808.jpg')
Instant_source('GEOCOLOR','10848x10848.jpg')

#++++++++++++++++++if ou wanna change resolution uncoment+++++++++++++++++++++++

    #   '339x339.jpg'          # essa imagem pesa 27kb
    #   '678x678.jpg'          # essa imagem pesa 96kb
    #   '1808x1808.jpg'        # essa imagem pesa 582kb
    #   '5424x5424.jpg'        # essa imagem pesa 4.13mb
    #   '10848x10848.jpg'      # essa imagem pesa 67.96mb

#++++++++++++++++++wanna check the url before open link? +++++++++++++++++++++++
