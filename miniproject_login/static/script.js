function login() {
    window.location.href = "/login"
}

function logout() {
    $.removeCookie('mytoken');
    alert('로그아웃!')
    window.location.href = '/'
}

function music_info() {
    alert("상세페이지test")
}

function heart_click() {
    alert("하트를 눌렀습니다!")
}

function post() {
    let url = $('#url-input').val()
    let genre = $('#genre-input').val()
    let today = new Date().toISOString()
    if (url == "") {
        alert("URL을 입력하세요!")
    } else {
        $.ajax({
            type: 'POST',
            url: '/posting',
            data: {url_give: url, date_give: today},
            success: function (response) {
                if (response['msg'] == '이미 등록된 URL입니다!') {
                    alert(response['msg'])
                } else {
                    alert(response['msg'])
                    window.location.reload()
                }
            }
        });
    }
}

function listing(username) {
    $('#card-div').empty()
    $.ajax({
        type: 'GET',
        url: `/posting`,
        data: {},
        success: function (response) {
            let rows = response['posts']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let artist = rows[i]['artist']
                let album_title = rows[i]['album_title']
                let album_img = rows[i]['album_img']
                let genre = rows[i]['genre']

                console.log(title, artist, album_img, album_title, genre)
                let temp_html = `<div class="album-card">
                                    <div class="album-img-div">
                                        <img src="${album_img}"
                                             class="album-img" onclick="music_info()">
                                        <i onclick="heart_click()" class="fa-solid fa-heart"></i>
                                    </div>

                                    <div class="album-item">
                                        <span class="music-title">${title}</span>
                                        <span class="music-artist">${artist}</span>
                                        <span class="album-title">${album_title}</span>
                                        <span class="album-genre" id="genre">${genre}</span>
                                    </div>
                                </div>`
                $('#card-div').append(temp_html)
            }
        }
    });
}

function genre(genre_key, genre_key2, genre_key3, username) {
    if (username == undefined) {
        username = ""
    }
    $('.album-card').remove()
    $.ajax({
        type: 'GET',
        url: `/posting?username_give=${username}`,
        data: {},
        success: function (response) {
            let rows = response['posts']
            for (let i = 0; i < rows.length; i++) {
                let title = rows[i]['title']
                let artist = rows[i]['artist']
                let album_title = rows[i]['album_title']
                let album_img = rows[i]['album_img']
                let genre = rows[i]['genre']
                let url = rows[i]['melon_url']
                let temp_html = `<div class="album-card" >
                                    <div class="album-img-div">
                                        <img src="${album_img}"
                                             class="album-img" onclick="music_info('${url}')">
                                        <i onclick="heart_click()" class="fa-solid fa-heart"></i>
                                    </div>

                                    <div class="album-item">
                                        <span class="music-title">${title}</span>
                                        <span class="music-artist">${artist}</span>
                                        <span class="album-title">${album_title}</span>
                                        <span class="album-genre" id="genre">${genre}</span>
                                    </div>
                                </div>`
                if (genre.includes(genre_key) || genre.includes(genre_key2) || genre.includes(genre_key3)) {
                    $('#card-div').append(temp_html)
                }
            }
        }
    });
}
