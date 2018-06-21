queue()
    /*
        -- GETTING THE DATA --
    */
    .defer(d3.json, "/goals")
    .await(makeGraphs);

function makeGraphs(error, goals){
    if (error) {
        console.log("Error receiving data-set with error: " + error.statusText);
        throw error;
    } else {
        console.log('Data object successfully received.')
    }

    /*
        -- CREATING THE GRAPHS --
    */

    // -- DEFINING THE DIMENSIONS AND GROUPS --
    var ndx = crossfilter(goals);

    /* goals attributes 
    goalscorer
    minute
    method
    round
    country
    continent
    phase
    */

    // Chart 1 dimension/group
    // Get the count of how many goals were scored by a particualar method throughout the tournament
    var methodOfGoalDim = ndx.dimension(function(d){ return d.method });
    var methodOfGoalGroup = methodOfGoalDim.group();

    // Chart 2 dimension/group
    var goalsPerMinuteDim = ndx.dimension(function(d){ return d.minute });
    var goalsPerMinuteRangeGroup = goalsPerMinuteDim.group(function(v){
        if(v <= 10) return "0-10";
        else if (v <= 20) return "11-20";
        else if (v <= 30) return "21-30";
        else if (v <= 40) return "31-40";
        else if (v <= 50) return "41-50";
        else if (v <= 60) return "51-60";
        else if (v <= 70) return "61-70";
        else if (v <= 80) return "71-80";
        else if (v <= 90) return "81-90";
        else if (v <= 100) return "91-100";
        else if (v <= 110) return "101-110";
        else return "111+";
    });

    // Chart 3 dimension/group
    // Get the count of how many goals were scored during a particular attacking phase throughout the tournament
    var phaseOfGoalDim = ndx.dimension(function(d){ return d.phase });
    var phaseOfGoalGroup = phaseOfGoalDim.group();
    
    // Chart 4 dimension/group
    // Get the top 5 goalscorers and their total goals
    var GoalscorersDim = ndx.dimension(function(d){ return d.goalscorer });
    var GoalsPerPlayerGroup = GoalscorersDim.group().reduceCount();
    
    // Chart 5 dimension/group
    // Get total goals scored by country
    var countryDim = ndx.dimension(function(d){ return d.country });
    var totalGoalsByCountryGroup = countryDim.group();

    // Chart 6 dimension/group
    // Get total goals scored by continent
    var continentDim = ndx.dimension(function(d){ return d.continent });
    var totalGoalsByContinentGroup = continentDim.group();
    
    // -- BUILDING THE CHARTS --
    
    // Chart 1 Build
    var totalGoalsByMethodPieChart = dc.pieChart('#total-goals-by-method-pie-chart')
        .dimension(methodOfGoalDim)
        .group(methodOfGoalGroup);
    
    // Chart 2 Build
    var goalsPerMinuteRowChart = dc.rowChart('#goals-per-minute-row-chart')
        .group(goalsPerMinuteRangeGroup)
        .dimension(goalsPerMinuteDim);
    
    // Chart 3 Build
    var totalGoalsByphasePieChart = dc.pieChart('#total-goals-by-phase-pie-chart')
        .dimension(phaseOfGoalDim)
        .group(phaseOfGoalGroup);
    
    // Chart 4 Build
    var goalscorersRowChart = dc.rowChart('#goalscorers-row-chart')
        .group(GoalsPerPlayerGroup)
        .dimension(GoalscorersDim)
        .ordering(function(d){return -d.value});
    
    // Chart 5 Build
    var totalGoalsByCountryPieChart = dc.pieChart('#total-goals-by-country-pie-chart')
        .dimension(countryDim)
        .group(totalGoalsByCountryGroup);
    
    // Chart 6 Build
    var totalGoalsByContinentPieChart = dc.pieChart('#total-goals-by-continent-pie-chart')
    .dimension(continentDim)
    .group(totalGoalsByContinentGroup);

        // Render the charts
    dc.renderAll();
}