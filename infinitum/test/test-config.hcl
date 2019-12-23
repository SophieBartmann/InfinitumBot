debug = true 
log_file = "./log.txt"

admins = ["global_admin"]

Bot "infinitumBot" {
    username = "infinitum"
    realname = "infinitum"
    admins = ["bot_admin"]
    server = "irc.freenode.net"
    port = 6697

    Channel "#infinitumbot" {
        modules = ["hangman", "glossary", "wikipedia"]
        entry_message = "huhu sagt der uhu"
        leave_message = "und tschüss"
        admins = ["channel_admin1", "channel_admin2"]
    }

    Channel "#infinitum2" {
        
    }

    Module "food.Waitress" {

    }

    Module "fun.Peace" {

    }
}
