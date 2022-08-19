import math
import folium
import json
import os,sys

now_dir = os.getcwd()

M = float(input('규모: '))

dep = 9.8

print('-'*20)
lon = float(input('위도: '))
lat = float(input('경도: '))
print('-'*20)

center = (lon,lat)

gal_mmi_kma = [0.51,0.68, 2.25, 7.44, 25.08, 67.22, 144.35, 310.26, 666.49, 1432.172] #기상청 진도표(기본은 %g라 *9.8해서 gal로 변환했음)
#0.51은 찐한 진도 1 가정

mmi_color = ['#B0B0B0', '#5e7e9b', '#6DA945', '#EDBA01', '#EC5C14', '#C40303', '#991B2D', '#8f192b','#6B1320','#3D0B12']


#울산원전부지(UJA-KEPRI05 모델-임창복 2006)
print('UJA-KEPRI05_2006')
c1= 28.29
c2= -1.975
c3= -6.73
c4= 0.606
c5= 4.889
c6= -0.046
c7= -1.002
c8= 0.027
c9 = 1

R0 = 50

new_m=folium.Map(location=center, zoom_start=7, tiles="cartodbpositron") #맵

new_y = []
mmi_b = -1
mmi_1top = False

for Repi in range(0,2000):
    #Repi(진앙거리)로 R(진원거리)를 구하는 과정인듯
    if M > 6.5:
        R = math.sqrt((Repi**2 + dep**2)*math.exp(2*(-1.25+0.22*M)))
    else:
        R = math.sqrt(Repi**2 + dep**2)


    lnY = c1 + c2*M+(c3+c4*M)*(math.log(R+c9*math.exp(c5))) + c6*(M-6)**2 + c7*math.log(min(R,R0)) + c8*math.log(max(R,R0)) #g

    Y = (math.exp(1)**(lnY))*980 #PGA(g)*980 = gal
    
    for i in range(10,0,-1): #진도 경계 확인용(2~10)
        if Y > gal_mmi_kma[i-1]: #기준 이상인지
            mmi_n = i
            if mmi_n == mmi_b-1 and mmi_n>0: #MMI가 이전보다 1 떨어지면
                folium.Circle([lon,lat],tooltip=f"진도 {mmi_b}",radius=(Repi-1)*1000,color=mmi_color[mmi_b-1]).add_to(new_m) #맵에 원그리기
                print(f'{Repi-1}km 진도{mmi_b}-PGA {round(Y,2)}gal')
            elif mmi_n == 1:
                if Y>=gal_mmi_kma[0]:
                    mmi_1top = True
        
            mmi_b = mmi_n
            break
        
        elif mmi_1top and Y<gal_mmi_kma[0]:
            folium.Circle([lon,lat],tooltip=f"진도 1(높은)",radius=(Repi-1)*1000,color=mmi_color[0]).add_to(new_m) #맵에 원그리기
            print(f'{Repi-1}km 진도{mmi_b}-PGA {round(Y,2)}gal')
            mmi_1top = False

print('='*20)

###Yun (2008) 감쇠식 _ PGA(100SPS)
print('Yun_2008-PGA(100SPS)')
c1= 30.519
c2= -1.653
c3= -6.5
c4= 0.474
c5= 5.294
c6= -0.065
c7= -1.101
c8= 0.063
c9 = 1

R0 = 50

new_mPga=folium.Map(location=center, zoom_start=7, tiles="cartodbpositron") #맵

mmi_b = -1
mmi_1top = False

for Repi in range(0,2000):
    #Repi(진앙거리)로 R(진원거리)를 구하는 과정인듯
    if M > 6.5:
        R = math.sqrt((Repi**2 + dep**2)*math.exp(2*(-1.25+0.22*M)))
    else:
        R = math.sqrt(Repi**2 + dep**2)


    lnY = c1 + c2*M+(c3+c4*M)*(math.log(R+c9*math.exp(c5))) + c6*(M-6)**2 + c7*math.log(min(R,R0)) + c8*math.log(max(R,R0)) #g

    Y = (math.exp(1)**(lnY))*980 #PGA(g)*980 = gal

    
    for i in range(10,0,-1): #진도 경계 확인용(2~10)
        if Y > gal_mmi_kma[i-1]: #기준 이상인지
            mmi_n = i
            if mmi_n == mmi_b-1 and mmi_n>0: #MMI가 이전보다 1 떨어지면
                folium.Circle([lon,lat],tooltip=f"진도 {mmi_b}",radius=(Repi-1)*1000,color=mmi_color[mmi_b-1]).add_to(new_mPga) #맵에 원그리기
                print(f'{Repi-1}km 진도{mmi_b}-PGA {round(Y,2)}gal')

            elif mmi_n == 1:
                if Y>=gal_mmi_kma[0]:
                    mmi_1top = True
        
            mmi_b = mmi_n
            break
        
        elif mmi_1top and Y<gal_mmi_kma[0]:
            folium.Circle([lon,lat],tooltip=f"진도 1(높은)",radius=(Repi-1)*1000,color=mmi_color[0]).add_to(new_mPga) #맵에 원그리기
            print(f'{Repi-1}km 진도{mmi_b}-PGA {round(Y,2)}gal')
            mmi_1top = False

print('='*20)


state_geo = 'skorea-provinces-geo.json'


folium.Choropleth(
    geo_data=state_geo,
    fill_color='gray',
    fill_opacity=0,
    line_opacity=0.4
    ).add_to(new_m)

folium.Choropleth(
    geo_data=state_geo,
    fill_color='gray',
    fill_opacity=0,
    line_opacity=0.4
    ).add_to(new_mPga)


new_m.save('./map_UJA-KEPRI05_2006.html')
new_mPga.save('./map_Yun_2008-PGA(100SPS).html')

os.system(f"python -m webbrowser -t \"{now_dir}\\map_UJA-KEPRI05_2006.html\"")
os.system(f"python -m webbrowser -t \"{now_dir}\\map_Yun_2008-PGA(100SPS).html\"")
