"use strict";

let mapSketch = {
	
};
function init() {

	// Build the map data model
	let mapData = buildmap();
	
	// Flatten data

	let flatData = [];

	for (let i = 0; i < mapData.length; i++) {
		flatData = flatData.concat(mapData[i]);
	}

	let massivForShowing = [];
	massivForShowing = flatData
	
	// Draw the d3 sketch
	draw(massivForShowing);

	mapSketch.myDataContainer = d3.select("body")
	
	.append("div")
	.attr("id", "myDataContainer");



	console.log(""); // here to place break points
};


function projectPoint (lat, lon) {

    // Albers equal-area conic projection

    lat = lat * Math.PI / 180;
    lon = lon * Math.PI / 180;

    let stdParallel1 	=  29.5 * Math.PI / 180,
    	stdParallel2 	=  45.5 * Math.PI / 180,
    	centerLat 		=  29.0 * Math.PI / 180,
    	centerLon 		= -98.6 * Math.PI / 180;

    let earthRad = 3959; // mi

    // calculate projection constants
    let n 		= (Math.sin(stdParallel1) + Math.sin(stdParallel2)) * 0.5,
    	c 		= Math.cos(stdParallel1) ** 2 + 2 * n * Math.sin(stdParallel1),
    	rho0 	= earthRad * Math.sqrt(c - 2 * n * Math.sin(centerLat)) / n;

   	// project
    let	rho 	= earthRad * Math.sqrt(c - 2 * n * Math.sin(lat)) / n,
    	theta 	= n * (lon - centerLon),
    	x 		= rho * Math.sin(theta),
    	y 		= rho0 - rho * Math.cos(theta);

    return [x, y];

};



function buildmap () {

	// Find min / max 

	let xMin =  Infinity,	// -1312.9
		xMax = -Infinity,	//  1419.9
		yMin =  Infinity,	//  -258.0
		yMax = -Infinity;	//  1578.8

	for (let i = 0; i < jsonData.length; i++) {

		let currentDataRecord = jsonData[i];

		let projected = projectPoint(currentDataRecord.lat, currentDataRecord.lon),
			x = projected[0],
			y = projected[1];

		if (x < xMin) { xMin = x; }
		if (x > xMax) { xMax = x; }
		if (y < yMin) { yMin = y; }
		if (y > yMax) { yMax = y; }

		currentDataRecord.x = x;
		currentDataRecord.y = y;
	}

	console.log(xMin, xMax, yMin, yMax);
		

	// Calculate bin step

	let	xSize 	= -(xMin) + (xMax) + 0.1,
		xBinNum = 100,
		binStep = xSize / xBinNum;
	
	// Calculate number of bins along y-axis

	let	ySize 	= -(yMin) + yMax + 0.1,
		yBinNum = Math.ceil(ySize / binStep);


	// Build the actual map structure

	let map = new Array(yBinNum);

	let xStart 	= xMin,
		yStart 	= yMax;

	for (let i = 0; i < yBinNum; i++) {

		map[i] = new Array(xBinNum);

		for (let j = 0; j < xBinNum; j++) {

			map[i][j] = {
				cellData: 	[], 
				x: 			xStart + binStep * j - binStep * 0.5,
				y: 			yStart - binStep * i + binStep * 0.5 //changed to +
			};
		}
	}


    // Place data into bins 

	for (let i = 0; i < jsonData.length; i++) {

		let currentDataRecord = jsonData[i];
		

		let xBin = Math.floor((currentDataRecord.x - xStart) / binStep),
			yBin = Math.floor((yStart - currentDataRecord.y) / binStep);

		
		map[yBin][xBin].cellData.push(currentDataRecord);
		
	}

	// Save map size data for the d3 sketch 

 	mapSketch.xMin = xMin;
 	mapSketch.xMax = xMax;
 	mapSketch.yMin = yMin;
 	mapSketch.yMax = yMax;

 	mapSketch.aspectRatio = ySize / xSize;

 	

 	for (let i = 0; i < yBinNum; i++) {
		for (let j = 0; j < xBinNum; j++) {

			let currentCell 	= map[i][j],
				dataCount 	= {col: 0};


			for (let i = 0; i < currentCell.cellData.length; i++) {

				let currentRecord = currentCell.cellData[i];

				
				if (currentRecord.color5) {
					dataCount.col = currentRecord.color5;
					
					
				}

				if (currentRecord.color1) {
					dataCount.col1 = currentRecord.color1;

				}

				if (currentRecord.color2) {
					dataCount.col2 = currentRecord.color2;

				}

				if (currentRecord.color3) {
					dataCount.col3 = currentRecord.color3;

				}

				if (currentRecord.color4) {
					dataCount.col4 = currentRecord.color4;

				}
			}

			currentCell.dataCount = dataCount;


	}}

	return map;

	};


//Draw map

function draw (massivForShowing) {

	var canvasWidth = 800,
		canvasHeight = 800,
		margin = 50;

	d3.select("svg").remove();

	//Create button

    
    

    
    //Create container for map
	var mainSvgGroup = d3.select("body")
		
		.append("svg")
			
			.attr("id", "svgCanvas")
			.attr("width", canvasWidth)
			.attr("height", canvasHeight)
			.append("g")
				.attr("transform", "translate(" + margin + "," + margin + ")");


	var mapWidth = 700,
		mapHeight = mapWidth * mapSketch.aspectRatio;

	var symbolRadius = 3,
		symbolFill = "#908a40"; //change the default color

	var xScale = d3.scaleLinear()
		.domain( [mapSketch.xMin, mapSketch.xMax])
		.range([0, mapWidth]);

	var yScale = d3.scaleLinear()
		.domain( [mapSketch.yMax, mapSketch.yMin])
		.range([0, mapHeight]);

 	
	var cellSymbols = mainSvgGroup.selectAll(".cell")
		.data(massivForShowing);
	  // create a tooltip    
	
	// Draw circles with color

	cellSymbols.enter()	
		.append("g")
			// .attr("class", "cell")
			.attr("id", "coloredCircle")
			.classed("cell", true)
			.classed("clickable", function (d) {

				if (d.cellData.length) {
					return true;
				}

					return false;
			})

			.each (function (d) {

													
				let dataDiv = d3.select(this);
				let circleDiv = dataDiv.append("circle");

				circleDiv.attr("cx", function (d) { return xScale(d.x); })
				circleDiv.attr("cy", function (d) { return yScale(d.y); })
				circleDiv.attr("r", symbolRadius)
				
				circleDiv.style("fill", function (d) {
					let color = "none";
					if (d.cellData.length>0){
									
									color = d.dataCount.col }
					
						return color;
		  	
				
				 })
				let circleDiv2 = dataDiv.append("circle");
				circleDiv2.attr("id","darkCircles")
				circleDiv2.attr("cx", function (d) { return xScale(d.x+15); })
				circleDiv2.attr("cy", function (d) { return yScale(d.y+15); })
				circleDiv2.attr("r", symbolRadius)
			
				circleDiv2.style("fill", function (d) {
					let color = "none";
					if (d.cellData.length>0){
								
								color = d.dataCount.col2 }
				
					return color;
				})
				let circleDiv1 = dataDiv.append("circle");
				circleDiv1.attr("id","darkCircles")
				circleDiv1.attr("cx", function (d) { return xScale(d.x+30); })
				circleDiv1.attr("cy", function (d) { return yScale(d.y+30); })
				circleDiv1.attr("r", symbolRadius)
			
				circleDiv1.style("fill", function (d) {
					let color = "none";
					if (d.cellData.length>0){
								
								color = d.dataCount.col1 }
				
					return color;
				})
				let circleDiv3 = dataDiv.append("circle");
				circleDiv3.attr("cx", function (d) { return xScale(d.x-15); })
				circleDiv3.attr("cy", function (d) { return yScale(d.y-15); })
				circleDiv3.attr("r", symbolRadius)
			
				circleDiv3.style("fill", function (d) {
					let color = "none";
					if (d.cellData.length>0){
								
								color = d.dataCount.col3 }
				
					return color;
				})
				let circleDiv4 = dataDiv.append("circle");
				circleDiv4.attr("cx", function (d) { return xScale(d.x+15); })
				circleDiv4.attr("cy", function (d) { return yScale(d.y+30); })
				circleDiv4.attr("r", symbolRadius)
			
				circleDiv4.style("fill", function (d) {
					let color = "none";
					if (d.cellData.length>0){
								
								color = d.dataCount.col4 }
				
					return color;
				})



			})


	

			//Clicking function for circles
		
	mainSvgGroup.selectAll(".cell")
	.on("click", function (d) {

				d3.selectAll(".image").remove();


				let filteredData = d.cellData.filter(function (d) {

					if (d.clicked) {
						return false;
					} else {
						return true;
					}
				});


				mapSketch.myDataContainer.selectAll(".image")
					.data(filteredData)
						.enter()

									.append("div")
									
											.classed("image",true)
											
												.each (function (d) {

													
													let myDataDiv = d3.select(this);
													let imgDiv = myDataDiv.append('div');
															imgDiv.classed("myDataPic",true);
														if (d.media) {
																	imgDiv.append("img")
																	.classed("image1",true)
																	.transition()
																		.delay(500)
		        														
																		.attr("src",d.media);	
																		console.log(d.coded1,d.coded2,d.coded3,d.coded4,d.coded5)
																	}

													let textBodyDiv = imgDiv.append("div");

													textBodyDiv.classed("textBody", true);

													textBodyDiv.append("div")
													.classed("cityName", true)
													.text(d.keyword);

													});
					
	
			});

	//Update selection when clicking on button
	mainSvgGroup.selectAll("circle")

	.on("dblclick", function(d){
	

			d3.select(this)
			.style("display","None")
			
	})


	//Update selection when clicking on button
	mainSvgGroup.selectAll("#darkCircles")

	.on("dblclick", function(d){
	

			d3.selectAll("#darkCircles")
			.style("display","None")
			
	})
};
		


					
								
function clickingOnPoint (massivForShowing) {
	
	for (let i = 0; i < massivForShowing.length; i++) { 
		if(i.cellData.coded1 <40){
				console.log(i.cellData.coded1)
				i.cellData.color1 = "Null"
		}
		else if(i.cellData.coded2 <40){
			i.cellData.color2 = "Null"
		}
		else if(i.cellData.coded3 <40){
			i.cellData.color3 = "Null"
		}
		else if(i.cellData.coded4 <40){
			i.cellData.color4 = "Null"
		}
	draw(massivForShowing)
	}
};



/// !!!!!!!!!!!КОНЕЦ!!!!!!!!!!!!!!!!


								// .on("click", function (d) {
								// 	console.log("click!")

								// 	if (d.clicked) {
								// 		d.clicked = false;

								// 	} else{
								// 		d.clicked = true;

								// 	}

								// 	let myDataDiv = d3.select(this);
								// 	myDataDiv.classed("clicked", d.clicked)

								// })
			





	
