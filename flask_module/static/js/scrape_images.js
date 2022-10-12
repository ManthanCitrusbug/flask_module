$("#get_all_images").on("click", function(){
    chrome.tabs.query({currentWindow: true, active: true}, function(tabs){
        $.ajax({
            url:"http://127.0.0.1:5000/scrape_images",
            method:"GET",
            data:{"url":tabs[0].url},
            success:function(data){
                console.log(data);
                $("#get_all_images").hide()
                for (let img in data){
                    $("body").append(`
                    <a class="btn"><img src="${data[img]}" alt="" class="scrape-images"></a>
                    `)
                }

                $(".scrape-images").on("click", function(){
                    var src = $(this).attr("src")
                    console.log(src, '=============== 18');
                    if (confirm("Wanna post this image?") === true){
                        $.ajax({
                            url:"http://127.0.0.1:5000/post_scraped_image",
                            method:"GET",
                            data:{"src":src},
                            success:function(data){
                                console.log(this.url, '===================== 23');
                            }
                        })
                    }
                })

            }
        })
    });
})