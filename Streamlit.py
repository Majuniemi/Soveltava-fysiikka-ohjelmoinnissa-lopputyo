import streamlit as st
import pandas as pd
import numpy as np
import folium 
from streamlit_folium import st_folium

url1 = "https://raw.githubusercontent.com/Majuniemi/Soveltava-fysiikka-ohjelmoinnissa-lopputyo/refs/heads/main/Location.csv"
url2 = "https://raw.githubusercontent.com/Majuniemi/Soveltava-fysiikka-ohjelmoinnissa-lopputyo/refs/heads/main/Linear%20Accelerometer.csv"
location_data = pd.read_csv(url1)
df_step = pd.read_csv(url2)

st.title('Fysiikan loppytyö - Matti Nieminen')

# Suodatetaan datojen alusta ensimmäiset 25 sekuntia pois
location_data = location_data.loc[location_data['Time (s)'] >= 25].reset_index(drop=True)
df_step = df_step.loc[df_step['Time (s)'] >= 25].reset_index(drop=True)

# Suodatetaan lopusta myös 2 sekuntia pois
location_data = location_data.loc[location_data['Time (s)'] <= location_data['Time (s)'].max()-2].reset_index(drop=True)
df_step = df_step.loc[df_step['Time (s)'] <= df_step['Time (s)'].max()-2].reset_index(drop=True)



# Suodatetaan datasta selvästi kävelytaajuutta suurempitaajuuksiset vaihtelut pois
# Filtteri
from scipy.signal import butter,filtfilt
def butter_lowpass_filter(data, cutoff, nyq, order):
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    y = filtfilt(b, a, data)
    return y

# Filttereiden parametrit:
T = df_step['Time (s)'][len(df_step['Time (s)'])-1] - df_step['Time (s)'][0] # Koko havaintoajan pituus
n = len(df_step['Time (s)']) # Havaintojen määrä
fs = n/T # Näytteenottotaajuus
nyq = fs/2 # Nyquist-taajuus
order = 3 # Kertaluku
cutoff = 1/(0.4) # Cut-off taajuus

filtered_signal = butter_lowpass_filter(df_step['Z (m/s^2)'], cutoff, nyq, order)

# Askelmäärä laskettuna suodatetusta kiihtyvyysdatasta
jaksot = 0
for i in range(len(filtered_signal)-1):
    if filtered_signal[i]/filtered_signal[i+1] < 0:
        jaksot = jaksot + 1
steps = np.floor(jaksot/2)

# Lisätään suodattimella saatu askelmäärä lopputuloksiin
st.write("Askelmäärä laskettuna suodatuksen avulla: ", steps, "askelta")



# Askelmäärä laskettuna Fourier-analyysin perusteella
f = df_step['Z (m/s^2)'] # Valittu signaali
t = df_step['Time (s)'] # Aika
N = len(df_step) # Havaintojen määrä
dt = np.max(t)/len(t) # Oletetaan sämpläystaajuus vakioksi

# Fourier-muunnos
fourier = np.fft.fft(f,N)
psd = fourier*np.conj(fourier)/N # Tehospektri
freq = np.fft.fftfreq(N,dt) # Taajuudet

# Rajataan pois nollataajuus ja negatiiviset taajuudet
L = np.arange(1,int(N/2))

# Lasketaan askelmäärä Fourier-analyysin perusteella
step_fft = freq[L][psd[L]==np.max(psd[L])][0] *np.max(t) # Askelmäärä

# Lisätään Fourierilla saatu askelmäärä lopputuloksiin
st.write("Askelmäärä laskettuna Fourier-analyysin avulla: ", step_fft, "askelta")



# Lasketaan kokonaismatka ja keskinopeus

# Lisätään keskinopeus lopputuloksiin
avg_speed = location_data['Velocity (m/s)'].mean()
avg_speed = round(avg_speed, 2)
st.write("Keskinopeus:", avg_speed, 'm/s' )



# Lasketaan kuljettu matka käyttäen Haversinen kaavaa
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    # Muunna asteet radiaaneiksi
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Haversine kaava
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Maapallon säde kilometreinä
    return c * r

# Määritellään latitudi ja longitudi erikseen
lat = location_data['Latitude (°)']
lon = location_data['Longitude (°)']

location_data['dist'] = np.zeros(len(location_data)) # Luodaan uusi sarake matkalle

# Peräkkäisten pisteiden väliset etäisyydet
for i in range(len(location_data)-1):
    location_data.loc[i,'dist'] = haversine(lon[i], lat[i],lon[i+1], lat[i+1])

# Lasketaan kokonaismatka
location_data['total_dist'] = np.cumsum(location_data['dist'])
total_distance = location_data['total_dist'].max()

# Lisätään kokonaismatka lopputuloksiin
total_distance = round(total_distance, 2)
st.write("Kuljettu matka: ", total_distance, "km")



# Laske askelpituus
step_length = (total_distance * 100000) / steps

# Lisätään askelpituus lopputuloksiin
step_length = round(step_length, 2)
st.write("Askelpituus: ", step_length, "cm")



# Piirretään kiihtyvyysdatan komponentti Z
st.subheader("Suodatettu kiihdytyvyysdatan komponentti Z")
df_step['Filtered Z (m/s^2)'] = filtered_signal
st.line_chart(df_step[['Time (s)', 'Filtered Z (m/s^2)']].set_index('Time (s)'), 
              y_label='Kiihtyvyyden komponentti Z', x_label='Aika (s)')



# Piirretään tehospektri
st.subheader("Tehospektri")
positive_freqs = freq[L]
positive_psd = np.abs(psd[L])
chart_data = pd.DataFrame({'Frequency (Hz)': positive_freqs, 'Power Spectral Density': positive_psd})
st.line_chart(chart_data.set_index('Frequency (Hz)'), y_label='Teho', x_label='Taajuus (Hz)')



# Piirretään kartta
st.subheader("Karttakuva")
start_lat = location_data['Latitude (°)'].mean()
start_long = location_data['Longitude (°)'].mean()
my_map = folium.Map(location = [start_lat,start_long], zoom_start = 18)
points = list(zip(location_data['Latitude (°)'], location_data['Longitude (°)']))
folium.PolyLine(points, color='blue', weight=2.5, opacity=1).add_to(my_map)
st_map = st_folium(my_map, width=900, height=650)