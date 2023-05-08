import streamlit as st
import streamlit as st
import numpy as np
import folium
import geopandas as gpd
from streamlit_option_menu import option_menu
from PIL import Image
from streamlit_folium import st_folium
from utils import popupTable
import branca
from pathlib import Path
import pandas as pd

from shapely.geometry import Point, Polygon

polygon_coordinates = [(77.39721140968196, 16.172619529979364),
(77.3980418982774, 16.242927699734754),
(77.33413458341393, 16.317682662029174),
(77.00729132169518, 16.675840851491426),
(76.53213263028893, 17.211819044626772),
(76.52510257276202, 17.219505188695333),
(76.27839387666094, 17.221220404307516),
(76.47203258152042, 16.991266605367716),
(76.74636602872643, 16.76001655307398),
(76.94961309903893, 16.49947813960339),
(77.22427130216393, 16.148909636763666),
(77.36160040372643, 16.111971285361168),
(77.39721140968196, 16.172619529979364)]



# Create a polygon object
polygon = Polygon(polygon_coordinates)
df = pd.read_csv('./static/sholapur_raichur.csv')
column1 = df['latitude']
column2 = df['longitude']

tuples = list(zip(column2,column1 ))

points_inside_polygon = []
for point in tuples:
    # Create a point object
    point_object = Point(point[0], point[1])

    # Check if the point is inside the polygon
    if polygon.contains(point_object):
        points_inside_polygon.append(point)


reversed_list = [t[::-1] for t in points_inside_polygon]

st.set_page_config(page_title='GalaxEye Space-Transmission Line Monitoring', page_icon='./static/galaxeye.png', layout="wide")




with st.sidebar:
 
    
    choose = option_menu("GALAXEYE LIVE", ["Dashboard","Vegetation Risk","Structural Risk","Environmental Risk","Report Generation","Drone Services"],
                        icons=['graph-up','tree','cloud-upload','cloud-haze2','book'],
                        menu_icon="cast", default_index=0,orientation="horizontal",
                         styles={
        "container": {"padding": "10!important", "background-color": "#26272F","font-size": "20px"},
        "icon": {"color": "white", "font-size": "20px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"10px", "--hover-color": "#0F1116"},
        "nav-link-selected": {"background-color": "#000000"},
    }
    )


dataframe = gpd.read_file("./static/map_indiGrid.geojson")
# lats = [20.83466574,20.83398309,20.76151577,20.80874355,20.83466517,20.81658646,20.71486564,20.8347532, 20.82000651,20.81548033]
# lons = [80.46099093,80.4599096,80.37233492,80.42676978,80.46081031,80.43631223,80.29681496,80.46180345,80.44361421,80.43559392]
# locations = list(zip(lats,lons ))
locations = reversed_list
vertices = [[ 16.172619529979364,77.3972114096819],
            [16.242927699734754,77.3980418982774],
            [16.317682662029174,77.33413458341393 ],
            [16.675840851491426,77.00729132169518],
            [17.211819044626772,76.53213263028893],
            [17.219505188695333,76.52510257276202],
            [17.221220404307516,76.27839387666094],
            [16.991266605367716,76.47203258152042],
            [16.76001655307398,76.74636602872643],
            [16.49947813960339,76.94961309903893],
            [16.148909636763666,77.22427130216393],
            [16.111971285361168,77.36160040372643],
            [16.172619529979364,77.39721140968196]]
    
verticesROW = [[ 20.840391123477904,80.46787412550168],
            [20.83557813303162,80.45688779737668],
            [20.821138238572644,80.44040830518918],
            [20.81022717812126,80.42427213575559],
            [20.761438666730143,80.36831052686887 ],
            [20.715203438844803,80.29277952100949 ],
            [20.693686402058262,80.26703031446652 ],
            [20.691116999565523,80.26943357374387 ],
            [20.71327666454747,80.2989593305798],
            [20.7604755769457,80.37517698194699], 
            [20.807338824024264,80.42873533155637 ],
            [20.818250093567354,80.44521482374387 ],
            [20.83172762988483,80.46238096143918] ,
            [20.836861612197165,80.47130735304074 ]]
logo = Image.open("./static/galaxeye.png")
if choose =="Dashboard":

    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:95px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title("Transmission Line Risk Assessment")
    with col2:
        st.image(logo, width=130 )

   

    col1, col2 = st.columns( [0.9,0.1])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #ffffff;} 
        </style> """, unsafe_allow_html=True)
        st.markdown('<p class="font">Area Of Interest</p>', unsafe_allow_html=True)    

    
        map = folium.Map(location=[16.754071892422, 76.85516009399588], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)


        for l, row in enumerate(dataframe.iterrows()):
                html = popupTable(dataframe, l)
                iframe = branca.element.IFrame(html=html,width=700,height=600)
                popup = folium.Popup(folium.Html(html, script=True), max_width=500)
                folium.GeoJson(data=row[1][0], popup=popup).add_to(map)
        
        
        for i in range(len(locations)):
                    folium.Marker(location=locations[i],
                    icon= folium.Icon(color='blue',
                    icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
        #polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)
        st_map = st_folium(map, width=1100, height=550)
        st.image(Image.open("./static/Dashboard_legend.png"),width=300 )

    # with col2 :
    #     st.image(Image.open("./static/Dashboard_legend.png"))



    
if choose =="Vegetation Risk":
    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:75px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title(choose)
    with col2:
        st.image(logo, width=130 )

    col1, col2,col3 = st.columns(3)
    with col1:
        
        Year = st.selectbox("Year", ["2023"])
    with col2:
        Month = st.selectbox("Month", ["Feb", "Mar", "Apr"])
    with col3:
        
        option_3 = st.selectbox("Insight", ["Encroachment Hotspots", "Land Cover Map"])

    Year = "2023"
    
    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #ffffff;} 
        </style> """, unsafe_allow_html=True)
        option_3_enc_text = "A Map with estimated height of vegetation in or around ROW is used to calculate the potential encroachment\
                                        hotspots. The legend shows the height of trees based on various thresholds in meters"
        option_3_LC_text = "A Land Classification map which shows the type of\
                                            vegetation cover(Trees, shrubs, crops, etc) in or around the ROW\
                                            region of the Transmission line."
        if option_3=="Encroachment Hotspots":
            st.markdown(f"<span style='font-size: 16px'>{option_3_enc_text}</span>", unsafe_allow_html=True)
        else:
            st.markdown(f"<span style='font-size: 16px'>{option_3_LC_text}</span>", unsafe_allow_html=True)

     

    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        map = folium.Map(location=[20.75710519982174,80.3587896427026], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
    
        folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='ArcGIS',
                name='Satellite',
                overlay=True,
                control=True).add_to(map)
        #folium.LayerControl().add_to(map)
        
        img = folium.raster_layers.ImageOverlay(
        name= option_3,
        image="./static/{}.png".format(Year+Month+option_3.split(' ')[0]+option_3.split(' ')[1]),
        bounds=vertices,
        opacity=1.0,
        interactive=True,
        cross_origin=False,
        zindex=1,
        )

        img.add_to(map)
        for i in range(len(locations)):
                folium.Marker(location=locations[i],
                   icon= folium.Icon(color='blue',
                   icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
    
            #folium.Marker(location=locations[i],radius=2,color='black').add_to(map)
        polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)

        st_map = st_folium(map, width=1100, height=550)
        folium.LayerControl().add_to(map)
       
        
   
    with col2:   
        
        if option_3 =="Land Cover Map":
            st.image(Image.open("./static/LandCover_legend.png"))
        else:
            st.image(Image.open("./static/2023FebEncroachmentHotspots_legend.png"))


elif choose =="Structural Risk":
    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:75px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title(choose)
    with col2:
        st.image(logo, width=130 )

    radio_style = "<style>div.row-widget.stRadio > div{flex-direction:row;font-size:70px;}</style>"
    
# Display the radio buttons with the custom CSS style
    st.markdown(radio_style, unsafe_allow_html=True)
   
    structural = st.radio("",["Land Subsidence","Potential Fouling Zones"])
    if structural =="Land Subsidence":
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(structural), unsafe_allow_html=True)   
            selected_ground_option_text = "The generated susceptibility map of land subsidence intensities can be used\
                                            to predict the high-susceptibility areas of different land subsidence\
                                            intensities along transmission lines ROW, which is important to the\
                                            planning, design, protection, and operations management of transmission\
                                            line towers.Transmission towers require a solid foundation to support their\
                                         weight and withstand external forces such as wind and seismic activity. \
                                            Foundation problems, such as settling or shifting, can cause towers to\
                                            become unstable and potentially collapse.\
                                            The movement of Towers causes seismic vibrations and it is important to \
                                            monitor the vibrations and take appropriate measures to reduce their impact on nearby structures."
            
            
            st.markdown(f"<span style='font-size: 16px'>{selected_ground_option_text}</span>", unsafe_allow_html=True)

            val = "This is a 1 year displacement map for 2022'March to 2023'March. The Transmission tower with at risk of\
                  loss of integrity with the ground is marked in red cirle in the map below"
            st.markdown(f"<span style='font-size: 12px'>{val}</span>", unsafe_allow_html=True)

            
        

        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            map = folium.Map(location=[16.754071892422, 76.85516009399588], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)
            #folium.LayerControl().add_to(map)
            
            img = folium.raster_layers.ImageOverlay(
            name= structural,
            image="./static/{}_indiG.png".format(('').join(structural.split(' '))),
            bounds=vertices,
            opacity=1.0,
            interactive=True,
            cross_origin=False,
            zindex=1,
            )

            img.add_to(map)
            for i in range(len(locations)):
                # if locations[i]==(20.71486564, 80.29681496):
                #     folium.CircleMarker(location=locations[i],radius=30,color='red',line_width=40, opacity=5).add_to(map)
                folium.Marker(location=locations[i],
                    icon= folium.Icon(color='blue',
                    icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
            polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)

            st_map = st_folium(map, width=1100, height=550)
            folium.LayerControl().add_to(map)
        
            

        with col2:               # To display brand log
      
            if structural == "Land Subsidence":
                st.image(Image.open("./static/{}_legend.png".format("LandSubsidence")))
    
    elif structural == "Potential Fouling Zones":
        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format(structural), unsafe_allow_html=True)   
            selected_ground_option_text = "An accurate PDM(pollution Distribution Maps) can help in optimising the\
                                        arrangement of monitoring points and promptly clean the more seriously\
                                        fouled insulators to ensure stable equipment operation."
            

            st.markdown(f"<span style='font-size: 16px'>{selected_ground_option_text}</span>", unsafe_allow_html=True)
            val = "The Transmission Towers in the region with high industrial Pollution value are more susceptible to\
                    flash-overs caused by fouling and are marked here with red circles"
            st.markdown(f"<span style='font-size: 12px'>{val}</span>", unsafe_allow_html=True)

    
        

        col1, col2 = st.columns( [0.8, 0.2])
        with col1:               # To display the header text using css style
            map = folium.Map(location=[16.754071892422, 76.85516009399588], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)
            #folium.LayerControl().add_to(map)
            
            img = folium.raster_layers.ImageOverlay(
            name= structural,
            image="./static/{}_indiG.png".format("PDM"),
            bounds=vertices,
            opacity=1.0,
            interactive=True,
            cross_origin=False,
            zindex=1,
            )

            img.add_to(map)
            for i in range(len(locations)):
                if locations[i]==(20.82000651, 80.44361421) or locations[i]==(20.83398309, 80.4599096):
                    folium.CircleMarker(location=locations[i],radius=30,color='red',line_width=50, opacity=5).add_to(map)
                    folium.Marker(location=locations[i],
                        icon= folium.Icon(color='blue',
                        icon_color='yellow',icon ="tower"),popup='Coordinates: {}, Max Pollution Density: 0.00053'.format(locations[i])).add_to(map)
                else:
                    folium.Marker(location=locations[i],
                        icon= folium.Icon(color='blue',
                        icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
            polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)
            

            st_map = st_folium(map, width=1100, height=550)
            folium.LayerControl().add_to(map)
        
            
        with col2:               # To display brand log
            val = "The PDM is in mol/meter-square"
            st.markdown(f"<span style='font-size: 16px'>{val}</span>", unsafe_allow_html=True)
            st.image(Image.open("./static/PollutionDistributionMap_legend.png"))



elif choose == "Environmental Risk":
    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:75px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title(choose)
    with col2:
        st.image(logo, width=130 )

    col1, col2,col3 = st.columns(3)
    with col1:
        Year = st.selectbox("Year", ["2023"])
    with col2:
        Month = st.selectbox("Month", ["Mar"])
    with col3:
        
        option_3 = st.selectbox("Insight", ["Fire Hotspots","Land Surface Temperature", "Vegetation Moisture Index"])

    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        st.markdown(""" <style> .font {
        font-size:35px ; font-family: 'Cooper Black'; color: #ffffff;} 
        </style> """, unsafe_allow_html=True)
        FireHotspots_text= "This map is used to identify drought conditions that pose a fire risk by correlating the\
                            vegetation and soil Moisture Index and the surface Temperature. The heat from the fire around the\
                                   region causes damage to the transmission line."
        LandSurfaceTemperature_text = "The Surface Temperature map here demonstrates the heat dispersion over the ROW, with a higher value \
                                        recorded when the intensity of radiation is higher. This is useful for identifying the\
                                              greenhouse effect in the area. A rise in Surface Temperature could lead to dry conditions."
        VegetationMoistureIndex_text = "The vegetation water content is calculated by NDMI, and water stress is indicated by the negative\
                                        values as they go closer to -1 and waterlogging as they get closer to +1. Thus, a\
                                             region's agronomic situation is addressed."

        if option_3 == "Fire Hotspots":
            option_3text = FireHotspots_text
        elif option_3 == "Land Surface Temperature":
            option_3text = LandSurfaceTemperature_text
        elif option_3 == "Vegetation Moisture Index":
            option_3text = VegetationMoistureIndex_text
            
    
        st.markdown(f"<span style='font-size: 16px'>{option_3text}</span>", unsafe_allow_html=True)
        


    

    col1, col2 = st.columns( [0.8, 0.2])
    with col1:               # To display the header text using css style
        if option_3 == "Land Surface Temperature":
            map = folium.Map(location=[20.75710519982174,80.3587896427026], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)
            #folium.LayerControl().add_to(map)
            
            img = folium.raster_layers.ImageOverlay(
            name= option_3,
            image="./static/Thermal.png",
            bounds=vertices,
            opacity=1.0,
            interactive=True,
            cross_origin=False,
            zindex=1,
            )

            img.add_to(map)
            for i in range(len(locations)):
                    folium.Marker(location=locations[i],
                    icon= folium.Icon(color='blue',
                    icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
        
            polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)

            st_map = st_folium(map, width=1100, height=550)
            folium.LayerControl().add_to(map)
        
        elif option_3 == "Vegetation Moisture Index":
            map = folium.Map(location=[20.75710519982174,80.3587896427026], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)
            #folium.LayerControl().add_to(map)
            
            img = folium.raster_layers.ImageOverlay(
            name= option_3,
            image="./static/MarchNDMI.png",
            bounds=vertices,
            opacity=1.0,
            interactive=True,
            cross_origin=False,
            zindex=1,
            )

            img.add_to(map)
            for i in range(len(locations)):
                    folium.Marker(location=locations[i],
                    icon= folium.Icon(color='blue',
                    icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
        
            polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)

            st_map = st_folium(map, width=1100, height=550)
            folium.LayerControl().add_to(map)

        elif option_3 == "Fire Hotspots":
            val = "The environmental fire prone areas are marked here with yellow circles"
            st.markdown(f"<span style='font-size: 12px'>{val}</span>", unsafe_allow_html=True)
            map = folium.Map(location=[20.75710519982174,80.3587896427026], zoom_start=11, scrollWheelZoom=True, tiles='Stamen Terrain')
        
            folium.TileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                    attr='ArcGIS',
                    name='Satellite',
                    overlay=True,
                    control=True).add_to(map)
            
            img = folium.raster_layers.ImageOverlay(
            name= option_3,
            image="./static/Correlation.png",
            bounds=vertices,
            opacity=1.0,
            interactive=True,
            cross_origin=False,
            zindex=1,
            )
            firespots = [(20.83541042217368,80.46141244556767),
                # (20.823537708019863,80.43961145069463),
                # (20.807652478456497,80.4353199162708),
                (20.775876998861502,80.39223291065557),
                # (20.76053615415873,80.34218411021307),
                (20.71282003372299,80.2982933534056)]
           
            
            img.add_to(map)
            for i in range(len(firespots)):
       
                folium.CircleMarker(location=firespots[i],radius=15,color='yellow',line_width=50, opacity=5).add_to(map)

            for i in range(len(locations)):
                folium.Marker(location=locations[i],
                icon= folium.Icon(color='blue',
                icon_color='yellow',icon ="tower"),popup='Coordinates: {}'.format(locations[i])).add_to(map)
        
                #folium.Marker(location=locations[i],radius=2,color='black').add_to(map)
            polygon = folium.Polygon(locations=verticesROW, color='black', fill_color=None, fill_opacity=1.0).add_to(map)

            st_map = st_folium(map, width=1100, height=550)
            folium.LayerControl().add_to(map)

        
        

    with col2:   
        
        if option_3 == "Fire Hotspots":
            st.image(Image.open("./static/Fire_legend.png"))


        elif option_3 =="Land Surface Temperature":
            st.image(Image.open("./static/LST_legend.png"))

            st.markdown(f"<span style='font-size: 14px'>The mean LST for this area</span>", unsafe_allow_html=True)
            meanval = "30.091 C"
            st.markdown(f"<span style='font-size: 35px'>{meanval}</span>", unsafe_allow_html=True)
        elif option_3 =="Vegetation Moisture Index":
            st.image(Image.open("./static/NDMI_legend.png"))
            st.markdown(f"<span style='font-size: 14px'>The mean Vegetation Moisture for this area</span>", unsafe_allow_html=True)
            meanval = "0.042"
            st.markdown(f"<span style='font-size: 35px'>{meanval}</span>", unsafe_allow_html=True)

            

elif choose =="Drone Services":
    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:75px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title("GalaxEye DROVCO")
    with col2:
        st.image(logo, width=130 )

    radio_style = "<style>div.row-widget.stRadio > div{flex-direction:row;font-size:70px;}</style>"
    
# Display the radio buttons with the custom CSS style
    st.markdown(radio_style, unsafe_allow_html=True)
   
    drone = st.radio("",["Vegetation Monitoring","Transmission Line Sagging"])
    if drone =="Vegetation Monitoring":
        col1,col2 = st.columns([0.85,0.15])
        with col1:
            st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format("3D Point Cloud"), unsafe_allow_html=True) 
            pt_cloud = Image.open("./static/3d_pc.png")
            video_file = open('./static/drone.webm', 'rb')
            video_bytes = video_file.read()
            drone = st.video(video_bytes)

            an = st.button('Show Analysis')
            #vid = st.button('3D point cloud')
            if an:
                
                drone.empty()
              
                pt = st.image(pt_cloud, caption='3D Encraochment analysis',use_column_width=True)
                
                an = st.button('Back to 3D point cloud video')
                if an:
                    video_file = open('./static/drone.webm', 'rb')
                    video_bytes = video_file.read()
                    drone = st.video(video_bytes)
                with col2 : 
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(" ")
                    st.markdown(f"<span style='font-size: 18px'>Mean Height</span>", unsafe_allow_html=True)
                    meanval = "6.54 m"
                    st.markdown(f"<span style='font-size: 35px'>{meanval}</span>", unsafe_allow_html=True)
                    st.markdown("""-------------------""")
                    st.markdown(f"<span style='font-size: 18px'>Highest Tree</span>", unsafe_allow_html=True)
                    meanval = "8.32 m"
                    st.markdown(f"<span style='font-size: 35px'>{meanval}</span>", unsafe_allow_html=True)
            # elif vid: 
              
            #     video_file = open('./static/drone.webm', 'rb')
            #     video_bytes = video_file.read()
            #     drone = st.video(video_bytes)
                # if st.button('Back to point cloud video'):
                #     pt.empty()
                #     video_file = open('./static/drone.webm', 'rb')
                #     video_bytes = video_file.read()
                #     drone = st.video(video_bytes)
                


            
            # pt_cloud = Image.open("./static/3d_pc.png")
            # st.image(pt_cloud, width=1000)
            # video_file = open('./static/drone.webm', 'rb')
            # video_bytes = video_file.read()
            # drone = st.video(video_bytes)

       

     
        # with col2:
    elif drone =="Transmission Line Sagging":
        col1,col2 = st.columns([0.8,0.2])
        with col1:
            st.markdown(""" <style> .font {
            font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
            st.markdown('<p class="font">{}</p>'.format("Radar Image for Transmission Lines"), unsafe_allow_html=True) 
            radar = Image.open("./static/dronesar.png")
            st.image(radar, width=1000)

        

    # st.markdown(""" <style> .font {
    # font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
    # </style> """, unsafe_allow_html=True)
    # st.markdown('<p class="font">{}</p>'.format("3D Point Cloud"), unsafe_allow_html=True) 
    # video_file = open('./static/drone.webm', 'rb')
    # video_bytes = video_file.read()
    # drone = st.video(video_bytes)

    # st.markdown(""" <style> .font {
    # font-size:30px ; font-family: 'Cooper Black'; color: #ffffff;} 
    # </style> """, unsafe_allow_html=True)
    # st.markdown('<p class="font">{}</p>'.format("Radar Image for Transmission Lines"), unsafe_allow_html=True) 
    # radar = Image.open("./static/dronesar.png")
    # st.image(radar, width=1000)




elif choose =="Report Generation":
    col1,col2 = st.columns([0.94,0.06])
    with col1:
        st.markdown(""" <style> .fonty {
            font-size:75px ; font-family: 'Cooper Black'; color: #ffffff;} 
            </style> """, unsafe_allow_html=True)
        st.title("Generate Report")
    with col2:
        st.image(logo, width=130 )

    col1, col2 = st.columns(2)
    with col1:
        
        Year = st.selectbox("Year", ["2023"])
    with col2:
        Month = st.selectbox("Month", ["Mar"])

       
  
    with open("./static/March_Report.xlsx", "rb") as template_file:
        template_byte = template_file.read()

    st.download_button(label="Download report",
                        data=template_byte,
                        file_name="./static/March_Report.xlsx",
                        mime='application/octet-stream')
    
