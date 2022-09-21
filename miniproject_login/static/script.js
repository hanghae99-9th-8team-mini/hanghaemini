        function login() {
            window.location.href = "/login"
        }

        function logout() {
            $.removeCookie('mytoken');
            alert('로그아웃!')
            window.location.href = '/'
        }

        function post() {
            let url = $('#url-input').val()
            let genre = $('#genre-input').val()
            if (url == "") {
                alert("URL을 입력하세요!")
            } else {
                $.ajax({
                    type: 'POST',
                    url: '/posting',
                    data: {url_give: url},
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
            if (username == undefined) {
                username = ""
            }
            $('#card-div').empty()
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

                        console.log(title, artist, album_img, album_title, genre)
                        let temp_html = `<div class="album-card" onclick="music_info()">
                                            <img src="${album_img}"
                                                 class="album-img">
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
