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

    // Get the count of how many goals were scored by a particualar method throughout the tournament
    var methodOfGoalDim = ndx.dimension(function(d){ return d.method });
    var methodOfGoalGroup = methodOfGoalDim.group();

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

    // Get the count of how many goals were scored during a particular attacking phase throughout the tournament
    var phaseOfGoalDim = ndx.dimension(function(d){ return d.phase });
    var phaseOfGoalGroup = phaseOfGoalDim.group();
    
    // Goalscorers dimension
    var GoalscorersDim = ndx.dimension(function(d){ return d.goalscorer });
    
    // Country dimension
    var countryDim = ndx.dimension(function(d){ return d.country });

    // Continent dimension
    var continentDim = ndx.dimension(function(d){ return d.continent });

    // Get total goals scored by round
    var roundDim = ndx.dimension(function(d){ return 'Round: ' + d.round });
    var totalGoalsByRoundGroup = roundDim.group();

    // Get the goals per minute
    var goalsPerSingleMinuteDim = ndx.dimension(function(d){ return d.minute });
    var goalsPerSingleMinuteGroup = goalsPerSingleMinuteDim.group();

    //----- FILTERS (select menus)

    var select = dc.selectMenu('#select-country')
        .dimension(countryDim)
        .group(countryDim.group());
        
    var select = dc.selectMenu('#select-goalscorer')
        .dimension(GoalscorersDim)
        .group(GoalscorersDim.group());
    
    var select = dc.selectMenu('#select-continent')
        .dimension(continentDim)
        .group(continentDim.group());
    
    
    // -- BUILDING THE CHARTS --

    // Chart attributes
    var colours = [
        '#F77', '#D66', '#C55', '#B44',
        '#A33', '#922', '#881212',
        '#711', '#660101', '#500'
    ]
    var width = 300;
    var height = 300;

    // Add extra width to row/line charts on larger devices
    var rowExtraWidth = 0
    if (window.outerWidth > 400){
        rowExtraWidth = 300;
    } else if (window.outerWidth > 600){
        rowExtraWidth = 600;
    };
    
    // PIE CHARTS
    // Goals by method pie-chart
    var totalGoalsByMethodPieChart = dc.pieChart('#total-goals-by-method-pie-chart')
        .dimension(methodOfGoalDim)
        .group(methodOfGoalGroup)
        .width(width)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    // Goals by phase pie-chart
    var totalGoalsByphasePieChart = dc.pieChart('#total-goals-by-phase-pie-chart')
        .dimension(phaseOfGoalDim)
        .group(phaseOfGoalGroup)
        .width(width)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    // Goals by round pie-chart
    var totalGoalsByRoundPieChart = dc.pieChart('#total-goals-by-round-pie-chart')
    .dimension(roundDim)
    .group(totalGoalsByRoundGroup)
    .width(width)
    .height(height)
    .colors(d3.scale.ordinal().range(colours));

    // ROW CHART Goals-per-minute (10 minute intervals)
    var goalsPerMinuteRowChart = dc.rowChart('#goals-per-minute-row-chart')
        .group(goalsPerMinuteRangeGroup)
        .dimension(goalsPerMinuteDim)
        .width(width+rowExtraWidth)
        .height(height)
        .colors(d3.scale.ordinal().range(colours));
    
    // Make goals-per-minute-chart read-only
    goalsPerMinuteRowChart.onClick = function(){};

    // LINE CHART goals-per-minute (minute-by-minute)
    var goalsPerMinuteLineChart = dc.lineChart('#goals-per-minute-line-chart');

    goalsPerMinuteLineChart
        .width(width+rowExtraWidth)
        .height(height)
        .x(d3.scale.linear().domain([
            0,
            130
        ]))
        .y(d3.scale.linear().domain([
            0,
            // Get the most frequent minute
            goalsPerSingleMinuteGroup.top(1)[0].value
        ]))
        .dimension(goalsPerSingleMinuteDim)
        .group(goalsPerSingleMinuteGroup)
        .xAxisLabel('minute scored')
        .colors('#F22');

    // RENDER THE CHARTS
    dc.renderAll();
}
