// 閉じるフラグ
var flag = true;

// プレイヤーをログアウトさせる
function del_player() {
    $(window).on("beforeunload", function () {
        if (flag) {
            var urlParams = new URLSearchParams(window.location.search);
            var result = $.isEmptyObject(urlParams);
            if (!result) {
                var player_name = urlParams.get("player_name");
                $.ajax({
                    url: "cgi-bin/ajax.py",
                    type: "POST",
                    async: false,
                    data: {
                        "func": "del_player",
                        "player_name": player_name
                    }
                })
            }
        }
    });
}

// ルームを生成する
function create_room() {
    $("#create_room").on("click", function (e) {
        e.preventDefault();
        var room_name = $("[name='room_name']").val();
        $("[name='room_name']").val("");
        console.log(room_name);
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            async: false,
            dataType: "json",
            data: {
                "func": "create_room",
                "room_name": room_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data);
                var urlParams = new URLSearchParams(window.location.search);
                var player_name = urlParams.get("player_name");
                var url = "htmls/room.html?room_name=" + room_name + "&player_name=" + player_name;
                flag = false;
                window.location.href = url;
            })
            .fail(function (data) {
                console.log("fails");
                console.log(data);
            });
    });
}

// プレイヤーを生成する
function create_player() {
    $("#create_player").on("click", function (e) {
        e.preventDefault();
        var player_name = $("[name='player_name']").val();
        $("[name='player_name']").val("");
        $.ajax({
            url: "cgi-bin/ajax.py",
            type: "POST",
            dataType: "json",
            // async: false,
            data: {
                "func": "create_player",
                "player_name": player_name
            }
        })
            .done(function (data) {
                console.log("success");
                console.log(data);
                var url = "?player_name=" + data["player_name"];
                var path = location.pathname;
                window.history.pushState(null, null, path + url);
                set_player_name();
            });
    });
}

// プレイヤー名をセットする
function set_player_name() {
    var urlParams = new URLSearchParams(window.location.search);
    var result = $.isEmptyObject(urlParams);
    if (!result) {
        var player_name = urlParams.get("player_name");
        $("#player_name").html(player_name);
    }
}

$(function () {
    set_player_name();
    create_player();
    create_room();
    del_player();
});