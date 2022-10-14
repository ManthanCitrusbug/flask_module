(function(){
    var images = document.getElementsByTagName("img")
    var img_list = []

    for (let img in images){
        img_list.push(images[img])
        
        $("body").append(`
            <a class="btn" href='http://127.0.0.1:5000/post_scraped_image/?src="${window.btoa(images[img]['src'])}"'><img src="${images[img]['src']}" alt=""></a>
        `)
    }
}) ()