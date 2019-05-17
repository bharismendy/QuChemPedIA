function html_converter() {
    var doc = new jsPDF();
    var html=window.document.getElementsByTagName("body")[0];
    alert (html);
    doc.fromHTML(html , 15, 15, {
        'width': 800
    });

    setTimeout(function(){
        doc.save('molecular_export');
    },2000);
}
function draw_canvas(value, smile) {
    var canvasH = $("#"+value).height();
    var canvasW = $("#"+value).width();
    let options = {width : canvasW,
        height : canvasH,
    };
    // Initialize the drawer
    let smilesDrawer = new SmilesDrawer.Drawer(options);
    SmilesDrawer.parse(smile, function(tree) {
        // Draw to the canvas
        smilesDrawer.draw(tree, value, 'light', false);
    });
}

function page_result(nbresults) {
    var urlParams = new URLSearchParams(window.location.search);
    var nbresult = nbresults;
    var result_per_page = null;
    if (urlParams.get('nbrpp') == null){
        result_per_page = 10;
    }
    else{
        result_per_page = urlParams.get('nbrpp');
    }
    var url = window.location.href;var actualPage = null;
    if (urlParams.get('page') == null){
        actualPage = 1;
    }
    else{
        actualPage = urlParams.get('page');
    }
    var actualSearch = urlParams.get('typeQuery');
    var nbrpages = Math.ceil(nbresult/result_per_page);
    /* fonction qui enlève le "InChi=" dans la donnée */
    $(".molecule_name").children().each(function(){
        if(this.id.split("_")[0] === "inchi"){
            $("#"+this.id+" span").html($("#"+this.id+" span").text().replace("InChI=",""));
        }
    });
    /* Fonction qui test la disponibilité d'une page */
    // On Initialize la page à 0 quand on arrive sur la page
    $(".content_btn_page").text("Page : "+actualPage+" / "+nbrpages);
    // On test si la page actuelle est inférieur à la page max
    if ( actualPage < nbrpages){
        $(".btn-next").removeClass('fa-disabled');
        $(".btn-next").click(function(){
            actualPage++;
            urlParams.set('page',actualPage);
            var newUrl = location.protocol + '//' + location.host + location.pathname + "?" + urlParams.toString();
            window.location.href = newUrl;
        });
    }
    else{
        $('.btn-next').addClass('fa-disabled');
    }
    // On test si la page actuelle est suppérieur à 0
    if( actualPage > 1 ) {
        $('.btn-previous').removeClass('fa-disabled');
        $(".btn-previous").click(function(){
            actualPage--;
            urlParams.set('page',actualPage);
            var newUrl = location.protocol + '//' + location.host + location.pathname + "?" + urlParams.toString();
            window.location.href = newUrl;
        });
    }else{
        $('.btn-previous').addClass('fa-disabled');
    }
}
