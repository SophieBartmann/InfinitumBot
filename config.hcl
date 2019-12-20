debug = true 
log_file = "./log.txt"

Bot "InfinitumDev" {
    server = "chat.freenode.net"
    port = 6697
    username = "infinitum"
    realname = "infinitum"
    admins = ["corvuscornix"]

    channel "#infinitum-bot" {
        modules = ["hangman", "glossary", "wikipedia"]
        entry_message = "huhu sagt der uhu"
        leave_message = "und tschüss"
        admins = ["modinarium", "ultramod"]
    }
}
