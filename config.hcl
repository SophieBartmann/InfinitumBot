debug = true 
log_file = "./log.txt"

Bot "InfinitumDev" {
    server = "chat.freenode.net"
    port = 6697
    username = "infinitum"
    realname = "infinitum"
    admins = ["corvuscornix"]
    
    Channel "#infinitum-bot" {
        modules = ["food.Waitress"]
        entry_message = "Huhu sagt der Uhu"
        leave_message = "und tschüss"
        admins = ["modinarium", "ultramod"]
    }

    Module "food.Waitress" {
        cookies = "./cookies.csv"
        drinks = "./drinks.csv"
        food = "./food.csv"
    }

}

