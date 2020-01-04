debug = true 
log_file = "./log.txt"

Bot "InfinitumDev42" {
    server = "chat.freenode.net"
    port = 6697
    username = "infinitum"
    realname = "infinitum"
    admins = ["Yana"]
    
    Channel "#infinitum-bot" {
        modules = ["food.Waitress", "url.URL_resolver"]
        entry_message = "Schuhu sagt der Uhu"
        leave_message = "und bye"
        admins = ["modinarium", "ultramod"]
    }

    Module "food.Waitress" {
        cookies = "../cookies.csv"
        drinks = "../drinks.csv"
        food = "../food.csv"
    }

    Module "url.URL_resolver"{

    }

}

