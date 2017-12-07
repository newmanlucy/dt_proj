webroot = "http://localhost:8000"
purlRoot = "http://purl.org/dth/"
duckietownRoot = "http://book.duckietown.org/master/duckiebook/"

jQuery.expr[':'].Contains = function(a,i,m){
    c = jQuery(a)
        .text()
        .toUpperCase()
        .indexOf(m[3].toUpperCase())>=0;
    return c;
};

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

MAX_SAMPLE_LEN = 360

function getPageInfo(url, query) {
    $.ajax({
        url: url,
        success: function(data, status, xhr) {
            var obj = $.parseHTML(data)
            var pageDiv = $.grep($(obj), 
                function(e) {return e.id=="not-toc";})[0];
            var pageTitle = $('h1', pageDiv).text();
            var sample = getSample($(pageDiv), query);
            var emphasized = emphasizeWord(sample, query);
            resultdiv = $('#searchresults');
            var searchitem = 
            `<h3> <a href="${url}"> ${pageTitle} </a></h3>
            <p class="resultP">${emphasized}</p>`;

            resultdiv.append(searchitem);
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function getSample(obj, query) {
    var sections = $('.without-header-inside', obj);
    var containsWord = $(`:Contains("${query}")`, sections);
    var sample = "";
    for (var i=0; i<containsWord.length; i++) {
        var containingText = $(containsWord[i])
            .text();
        sample += containingText + "... ";
        if (sample.length >= MAX_SAMPLE_LEN) {
            break;
        }
    }
    sample = sample.substr(0, sample.length-3);
    if (sample.length > MAX_SAMPLE_LEN) {
        sample = sample.substr(0, MAX_SAMPLE_LEN);
        sample = sample.substr(0, 
            Math.min(sample.length, sample.lastIndexOf(" ")));
    }
    if (sample == "") {
        // TODO
        // Look at entire doc not filtered by 
        // .without-header-inside
    }
    if (sample.substr(-1) != '.') {
        sample += "...";
    }
    return sample;
}

function locations(substring,string) {
    var a = [];
    var i = -1;
    while((i=string.indexOf(substring,i+1)) >= 0) a.push(i);
    return a;
}

function emphasizeWord(string, query) {
    var stringLower = string.toLowerCase();
    var queryLower = query.toLowerCase();
    var locs = locations(queryLower, stringLower);
    var emphasized = "";
    var wlen = query.length;
    if (locs == []) {
        return string;
    }
    else {
        emphasized += string.substr(0, locs[0]);
        locs.push(string.length);
    }
    for (var i=0; i<locs.length; i++) {
        emphasized += `<b>${string.substr(locs[i], wlen)}</b>`;
        emphasized += string.substring(locs[i] + wlen, locs[i+1]);
        console.log(string.substr(locs[i+1], wlen));
    }
    return emphasized;
}

searchval = getParameterByName("searchbox");

$.getJSON(webroot + "/index.json", function(json) {
    idx = lunr.Index.load(json);
    result = idx.search(searchval);
    $('#searchbox').val(searchval);

    var resultdiv = $('#searchresults');
    if (result.length === 0) {
        // Hide results
        resultdiv.hide();
    } else {
        // Show result
        resultdiv = $('#searchresults');
        resultdiv.empty();
        var numResults = result.length
        var MAX_RESULTS_LEN = 10;
        resArray = []
        for (var i=0; i<numResults; i+=MAX_RESULTS_LEN) {
            resArray.push(result.slice(i, 
                Math.min(i+MAX_RESULTS_LEN,numResults)));
        }
        currentPage = 0;
        numPages = numResults / MAX_RESULTS_LEN;
        for (var i=0; i<numPages; i++) {
            var span = `<span id="result${i}span" 
                style="display:inline-block; padding:10px;">
                </span>`
            var show = `<a class="pageNumLink" id="link${i}"
                onclick="displayResults(${i},${numResults})" 
                href="javascript:void(0);">${i+1}</a>`
            $('#pageLinks').append(span);
            $(`#result${i}span`).append(show);

        }
        displayResults(currentPage, numResults);
    }
});

function displayResults(pageToDisplay, numResults) {
    var resultdiv = $('#searchresults');
    $(`#link${currentPage}`).removeClass('thisPageNumLink');
    $(`#link${pageToDisplay}`).addClass('thisPageNumLink');
    result = resArray[pageToDisplay];
    var numToDisplay = result.length;
    var msg = `<p> <em> 
        Showing items ${pageToDisplay*10+1} to 
        ${pageToDisplay*10+result.length} of 
        ${numResults} results </em></p>`;
    $('#showing').html(msg);
    resultdiv.empty();
    for (var item in result) {
        var ref = result[item].ref;
        var link = getURL(duckietownRoot, ref);
        var info = getPageInfo(link, searchval);
    }
    resultdiv.show();
    currentPage = pageToDisplay;
}
