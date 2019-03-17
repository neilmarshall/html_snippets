function titleCase(words) {
    words = words.toLowerCase().split(' ');
    return (words.map(word => word.charAt(0).toUpperCase() + word.slice(1))).join(' ');
}


function build_chart(data, selector) {
    var values = data.map(d => d[1]);
    var scaler = d3.scaleLinear()
                   .domain([0, d3.max(values)])
                   .range([0, 100]);
    d3.select(selector)
      .selectAll("div")
      .data(data)
      .enter()
      .append("div")
      .style("width", function(d) { return scaler(d[1]) + "%"; })
      .text(function(d) { return titleCase(d[0]); });
}
