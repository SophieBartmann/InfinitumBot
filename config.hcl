debug = true 
log_file = "./log.txt"

Bot "InfinitumDev" {
    username = "infinitum"
    realname = "infinitum"
    admins = ["corvuscornix"]

    channel "#infinitumbot" {
        modules = ["hangman", "glossary", "wikipedia"]
        entry_message = "huhu sagt der uhu"
        leave_message = "und tschüss"
        admins = ["modinarium", "ultramod"]
    }
}
