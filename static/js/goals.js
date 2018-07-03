// Toggle help function
var helpElements = document.getElementsByClassName('help');

var toggleHelp = function(){
    for (i = 0; i < helpElements.length; i++){
        if (helpElements[i].style.display == 'none'){
            helpElements[i].style.display = 'flex';
        } else {
            helpElements[i].style.display = 'none';
        }
    };
};

/*
    ***
        -- GRAPHS FOR GOAL STATS --
    ***
*/
queue()
    /*
        -- GETTING THE DATA --
    */
    .defer(d3.json, "/goalsdata")
    .await(makeGoalGraphs);

function makeGoalGraphs(error, goals){
    if (error) {
        console.log("Error receiving data-set with error: " + error.statusText);
        throw error;
    } else {
        console.log('goals object successfully received.')
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
    // Get the time a goal was scored using 10 minute intervals
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

    // Chart 7 dimension/group
    // Get total goals scored by round
    var roundDim = ndx.dimension(function(d){ return 'Round: ' + d.round });
    var totalGoalsByRoundGroup = roundDim.group();

    //----- Filters (select menus)

    var select = dc.selectMenu('#select-country')
        .dimension(countryDim)
        .group(countryDim.group());
        
    var select = dc.selectMenu('#select-goalscorer')
        .dimension(GoalscorersDim)
        .group(GoalscorersDim.group());
    //-----
    
    // -- BUILDING THE CHARTS --
    var colours = [
        '#F77', '#D66', '#C55', '#B44',
        '#A33', '#922', '#881212',
        '#711', '#660101', '#500'
    ]
    var width = 300;
    var height = 300;

    var rowExtraWidth = 0
    if (window.outerWidth > 400){
        rowExtraWidth = 300;
    } else if (window.outerWidth > 600){
        rowExtraWidth = 600;
    };
    
    // Chart 1 Build
    var totalGoalsByMethodPieChart = dc.pieChart('#total-goals-by-method-pie-chart')
        .dimension(methodOfGoalDim)
        .group(methodOfGoalGroup)
        .width(width)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    // Chart 2 Build
    var goalsPerMinuteRowChart = dc.rowChart('#goals-per-minute-row-chart')
        .group(goalsPerMinuteRangeGroup)
        .dimension(goalsPerMinuteDim)
        .width(width+rowExtraWidth)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    // Make chart read-only
    goalsPerMinuteRowChart.onClick = function(){};
    
    // Chart 3 Build
    var totalGoalsByphasePieChart = dc.pieChart('#total-goals-by-phase-pie-chart')
        .dimension(phaseOfGoalDim)
        .group(phaseOfGoalGroup)
        .width(width)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    
    // Chart 7 Build
    var totalGoalsByRoundPieChart = dc.pieChart('#total-goals-by-round-pie-chart')
    .dimension(roundDim)
    .group(totalGoalsByRoundGroup)
    .width(width)
    .height(height)
    .colors(d3.scale.ordinal().range(colours));


    // Render the charts
    dc.renderAll();
}

