From https://www.linkedin.com/search/results/all/?keywords=%23lightbim&origin=HASH_TAG_FROM_FEED&sid=.zr

# LightBIM and Speckle to bridge the gap between geotechnical and structural engineering 🌉

⛓️‍💥 Gap 1: Unstructured Data
Examples of unstructured, i.e. non-machine readable data: pdf's (with comments), messy Excels, sloppy CAD with annotations.
Problem: you need to sort out this data mess every time you need to do something. 🍕 It's a bit like putting all ingredients in one big bowl and then trying to bake different types of pizzas.

🌉 Bridge 1: LightBIM
LightBIM is the representation of AEC data with minimal geometry + attributes (the I in BIM). With this minimal BIM, AEC data can be structured and efficiently exchanged no matter the data type, workflow step or project stage.
For Example, a foundation pile is represented by a line with pile attributes attached.
BIM ≠ Revit

⛓️‍💥 Gap 2: Data Integration
A lot of our data is "held hostage" in software-specific (proprietary) file formats. Besides, analysis & modelling software often use a local coordinate reference system, whereas geotechnical data has real world coordinates.

🌉 Bridge 2: Speckle Connectors
Speckle is "The OpenSource Platform For 3D Data".
Speckle's connectors are plugins for many software we commonly use in AEC (read bridge 3). With the connectors you can send, i.e. upload your data "held hostage" in any of these software to Speckle and receive, i.e. download it in another one. Even if there is no connector for the software you work with, YourSoftware → Speckle or Speckle → YourSoftware is still possible with a bit of Grasshopper and/or Python scripting.
Let's go OpenBIM 🤩
OpenBIM ≠ IFC

⛓️‍💥 Gap 3: Data Visualization
Visualizing ground conditions and uncertainties together with structural elements in 3D has always been very challenging. This ultimately leads to suboptimal designs and problems such as cost & time overruns.

🌉 Bridge 3: Speckle Web App
All data in Speckle can be visualized together, i.e. federated, in @Speckle's Web App, no matter the software in which that data was generated.
Explore the public Speckle project from the second image yourself by following the link in the first comment 👇
That Speckle project contains data from Civil3D, Revit, Dynamo, Rhino, Grasshopper, QGIS, IFC and Python 

📆 In June I presented the above at the EAGE (European Association of Geoscientists and Engineers) annual conference in Oslo. See third image and these conference precedings: https://lnkd.in/gNhs9CNa

Acknowledgements:
- NGI - Norwegian Geotechnical Institute: BIM for GeoSciences webinars
- Mats Svensson from Tyréns AB: Geo-BIM for optimal use of geotechnical data (2016)
- Ramon van der Heijden: Building Information Generation & LightBIM
- Rory McCully, Joseph Landers, John Kuyt, Thomas Bush, Ben Gilson: How to put ComputationalDesign into practice in GeotechnicalEngineering

⛓️‍💥 Gap 4: Spatial Database Integration
While file-based workflows are common, they can become unwieldy when dealing with large amounts of geotechnical data across multiple projects. Traditional databases often lack robust support for spatial data types and geographic operations.

🌉 Bridge 4: PostGIS Integration
PostGIS extends PostgreSQL to provide enterprise-grade spatial database capabilities that complement the LightBIM and Speckle workflow:

- Store geotechnical data (boreholes, soil layers, test results) with proper spatial indexing
- Transform between different coordinate reference systems (CRS)
- Perform spatial queries and analysis on your geotechnical data
- Integrate with QGIS and other GIS tools that support PostGIS
- Enable multi-user collaboration on large datasets

Example workflow:
1. Import geotechnical data into PostGIS using Python/SQL
2. Use Speckle connectors to visualize PostGIS data alongside structural models
3. Perform spatial analysis (e.g., nearest neighbor searches for boreholes)
4. Export filtered/analyzed data back to engineering tools via Speckle

This creates a robust data backbone for your geotechnical engineering workflows while maintaining the flexibility of LightBIM and Speckle for visualization and exchange.


