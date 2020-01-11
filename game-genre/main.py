import analyse
import scrape

start_index = 11
cntr = start_index
max_iter = 340
has_next = True

if __name__ == "__main__":
    print(f"Starting to download more stuff. Starting with {start_index}, planning {max_iter} iterations end with {start_index + max_iter}.")
    while has_next and cntr < start_index + max_iter:
        try:
            has_next = scrape.get_games(cntr)
        except Exception:
            print(f"Something went wrong. Currently at index {cntr}. Started at {start_index} and planning {max_iter} iterations go until {start_index + max_iter}")
            raise
        print(f"Done with page {cntr}.")
        cntr += 1

    print(f"Finished up. Started with {start_index}, ended with {cntr}.")