// function buildMetadata(sample) {

//   // @TODO: Complete the following function that builds the metadata panel

//   // Use `d3.json` to fetch the metadata for a sample
  
//   d3.json(`/metadata/${sample}`).then(function(data) {

//     console.log('metatest: ', data);
  
//     // Use d3 to select the panel with id of `#sample-metadata`
//   d3.select("#sample-metadata").html("")
//   d3.select("#sample-metadata").append("tbody").html("")

//     // Use `.html("") to clear any existing metadata

//     for (const [key, value] of Object.entries(data)) {
//      // console.log(`${key} ${value}`); 
//      d3.select("tbody")
//      .append("tr")
//      .html(`<td>${key}:</td><td>${value}</td>`)
//     }
//     // Use `Object.entries` to add each key and value pair to the panel
//     // Hint: Inside the loop, you will need to use d3 to append new
//     // tags for each key-value in the metadata.
//   });
//     // BONUS: Build the Gauge Chart
//     // buildGauge(data.WFREQ);
// }



function buildCharts(city) {
  var today = new Date();
  var dd = today.getDate();
  var mm = today.getMonth()+1; //January is 0!
  var yyyy = today.getFullYear();



 var startMonth = String(mm);
 var dateAry = [];
 
 if (dd >= 1 && dd <= 7) {startMonth = startMonth + '-wk1'}
 else if (dd >= 8 && dd <= 14) {startMonth = startMonth + '-wk2'}
 else if (dd >= 15 && dd <= 21) {startMonth = startMonth + '-wk3'}
 else {startMonth = startMonth + '-wk4'}

 

 console.log('dates: ', startMonth);

  //var teststring = `/cities/${city}`
  //console.log('butt1: ', teststring);
    d3.json(`/cities/${city}`).then(function(data) {

     console.log('test999: ', data);

     var graphDate = [];
     var graphWk = ''

     for (var k = 0; k < data.Date.length; k++) {
      var dteStr = data.Date[k].split("/");
      
      //adjust month to 2 digits
      if (parseInt(dteStr[0]) >= 1 && parseInt(dteStr[0]) <= 9) {dteStr[0]  = '0' + dteStr[0] }
       // week 1 week 2 logic
       if (parseInt(dteStr[1]) >= 1 && parseInt(dteStr[1]) <= 7) {graphDate[k] = dteStr[0] + '-WK1'}
       else if (parseInt(dteStr[1]) >= 8 && parseInt(dteStr[1]) <= 14) {graphDate[k] = dteStr[0] + '-WK2'}
       else if (parseInt(dteStr[1]) >= 15 && parseInt(dteStr[1]) <= 21) {graphDate[k] = dteStr[0] + '-WK3'}
       else {graphDate[k] = dteStr[0] + '-WK4'}

      // adjust montyh 2 2 digits 
      if (parseInt(dteStr[1]) >= 1 && parseInt(dteStr[1]) <= 9) {dteStr[1]  = '0' + dteStr[1] }
             
      
       data.Date[k] = dteStr[2] + '-' + dteStr[0] + '-' + dteStr[1]

          
     }

     // add graphDate element to data object
     data['graphDate'] = graphDate;

     console.log('test99: ', data);



    const classLabels = ["Sports", "Music", "Arts & Theatre",  "Miscellaneous", "Film"];
    var classValues = [0,0,0,0,0];

    for (var i = 0; i < data.Classification.length; i++) {
   
      switch (data.Classification[i]) {
        case "Sports":
          classValues[0] += 1;
          break;
          case "Music": 
          classValues[1] += 1;
          break;
          case "Arts & Theatre":
          classValues[2] += 1;
          break;
          case "Miscellaneous":
          classValues[3] += 1;
          break;
          case "Film":
          classValues[4] += 1;
          break;
      }  
    }
    
    console.log(city, classValues)
    
      
     
 

//    const idsSlice = data.otu_ids.slice(0, 10);
//    const sampValSlice = data.sample_values.slice(0, 10);
//    const lblsSlice =  data.otu_labels.slice(0, 10);
// console.log('scliced: ', sampValSlice);

   

  var trace1 = {
   labels: classLabels,
   values: classValues,
   type: 'pie',
   text: classLabels
 };

 var data2 = [trace1];

// var layout = {
//   title: "'Bar' Chart",
// };

 Plotly.newPlot("pie", data2);





    });
  }   

//   // @TODO: Use `d3.json` to fetch the sample data for the plots
//   // d3.json(`/samples/${sample}`).then((data) => {
//   //   console.log(data);
//   //   });
//   // const dataPromise = d3.json(`/samples/${sample}`).then(function(data){
//   //   buildPie(data);

//   // });  
  
  


//   d3.json(`/samples/${sample}`).then(function(data) {

//     console.log('test1: ', data);
    



//     var ids = data.otu_ids
//     var sample_val = data.sample_values  
//     var txtLables = data.otu_lables

//     //var sortObj = data

//     console.log('otu: ', ids[0]);
//     console.log('samps: ', sample_val[0]);
    
//     var trace1 = {
//       type: "scatter",
//       mode: "markers",
//       name: ids,
//       x: ids,
//       y: sample_val,
//       text : txtLables,
//       marker: {
//         color: ids,
//         size: sample_val
//       }
//     };

//      var data1 = [trace1];

//      var layout = {
//       title: "Sample Data",
//       xaxis: { title: "OTU ID" }
//     };
     

//     // var layout = {
//     //   title: `${stock} closing prices`,
//     //   xaxis: {
//     //     range: [startDate, endDate],
//     //     type: "date"
//     //   },
//     //   yaxis: {
//     //     autorange: true,
//     //     type: "linear"
//     //   }

//     Plotly.newPlot("bubble", data1, layout);

//    // buildPie(data);

//    // sortObj.sort((a, b) => Number(b.sample_values) - Number(a.sample_values));

//    const idsSlice = data.otu_ids.slice(0, 10);
//    const sampValSlice = data.sample_values.slice(0, 10);
//    const lblsSlice =  data.otu_labels.slice(0, 10);
// console.log('scliced: ', sampValSlice);

   

//   var trace1 = {
//    labels: idsSlice,
//    values: sampValSlice,
//    type: 'pie'
//   // text: lblsSlice
//  };

//  var data2 = [trace1];

// // var layout = {
// //   title: "'Bar' Chart",
// // };

//  Plotly.newPlot("pie", data2);


//     });


    // @TODO: Build a Bubble Chart using the sample data

    // @TODO: Build a Pie Chart
    // HINT: You will need to use slice() to grab the top 10 sample_values,
    // otu_ids, and labels (10 each).
   
   

    // const dataPromise = d3.json(`/samples/${sample}`);
    // console.log("Data Promise: ", dataPromise);
    // console.log("data: ", dataPromise.promiseValue.otu_ids)
   
//}

function init() {
  var firstCity = 'Kansas City'
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");
   //selector.on("change", optionChanged );
  // Use the list of sample names to populate the select options

  d3.json("/names").then(function(cityNames) {
      
     for (var j = 0; j < cityNames.city.length; j++) {
       //console.log('test99: ', cityNames.baloney[j]);
       //     cityNames.forEach((city) => {
      selector
        .append("option")
        .text(cityNames.city[j])
        .property("value", cityNames.city[j]);
     }
     firstCity =  cityNames.city[0];
     //console.log('t99:', firstCity);

    });
    //console.log('t100:', firstCity);
   

     buildCharts(firstCity);


   }

//   d3.json("/names").then((cityNames) => {
//     cityNames.forEach((city) => {
//       selector
//         .append("option")
//         .text(city)
//         .property("value", city);
//     });
    
//     // Use the first sample from the list to build the initial plots
//      const firstCity = cityNames[0];
//     //     console.log('t1:', firstCity);

//      buildCharts(firstCity);
// //   //  buildMetadata(firstCity);
//    });
// }

function optionChanged(newCity) {
  // Fetch new data each time a new sample is selected
  console.log(newCity);
  buildCharts(newCity);
//  buildMetadata(newCity);
}

// Initialize the dashboard
init();
