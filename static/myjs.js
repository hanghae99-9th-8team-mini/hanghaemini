function post() {
    let comment = $("#textarea-post").val()
    let today = new Date().toISOString()
    $.ajax({
        type: "POST",
        url: "/posting",
        data: {
            comment_give: comment,
            date_give: today
        },
        success: function (response) {
            $("#modal-post").removeClass("is-active")
            window.location.reload()
        }
    })
}

function listing(username) {
    if (username == undefined) {
        username = ""
    }
    $("#cards-box").empty()
    $.ajax({
        type: "GET",
        url: `/get_posts?username_give=${username}`,
        data: {},
        success: function (response) {
                let rows = response["posts"]
                for (let i = 0; i < rows.length; i++) {
                    let image = posts[i]['image']
                    let title = posts[i]['title']
                    let artist = posts[i]['artist']
                    let album = posts[i]['album']
                    let genre = rows[i]['genre']

                    let html_temp = `<div class="col">
                                                <div class="card">
                                                    <img src="${image}"
                                                         class="card-img-top" alt="...">
                                                    <div class="card-body">
                                                        <span class="music-title">${title}</span>
                                                        <span class="music-artist">${artist}</span>
                                                        <span class="album-title">${album}</span> 
                                                        <span class="album-genre" id="genre">${genre}</span>                                                
                                                    </div>                                                                                          
                                            </div>                                   
                                    </div>`
                    $("#cards-box").append(html_temp)
                }
            }
    })
}
