# Capture the Flag (CTF) challenge

Learning about web security, network analysis, and problem-solving.

## Attach plan:


*   **Use of Tools:** `twython`, `tcpdump`, `strings`, `hashcat`, `apktool`, `jadx`, `fdisk`, `mount`, `nmap`, `netcat`, `curl`, `Burp Suite`, `Tampermonkey`, `git`, `wget`, `Audacity`, and more.  This exposure to different tools is invaluable.
*   **Proper Command Syntax:** The use of `root@kali:~/` prompts simulates a real hacking environment.
*   **Logical Progression:** The challenge is structure. Each section builds upon the previous ones.
*   **Google Search:** This is incredibly important because it emphasizes that even experienced people use search engines as a primary tool.  It normalizes the process of looking things up.


1.  **Twitter API Keys (CONSUMER_KEY, etc.):** warning:

    *   **"IMPORTANT: DO NOT include your actual Twitter API keys in a public write-up or repository.  Replace them with empty strings (as you have done) or placeholders like `YOUR_CONSUMER_KEY_HERE`.  Sharing API keys is a security risk."**

2.  **Hashcat Mode:** `-m 1800` for Hashcat, meaning:  `This specifies the hash type as sha512crypt (Unix).`

3.  **`find` Command Optimization:**  tediousness of navigating the directory structure. While manually navigating is a fun, educational exercise, you could use the more efficient `find` command:

    ```zsh
    find . -path "./home/elf/.doormat/. / /\/\/Don't Look Here!/You are persistent, aren't you?/'/key_for_the_door.txt" -print
    ```

    Or, even better, since you know the filename:

    ```zsh
    find . -name "key_for_the_door.txt" -print
    ```

    This demonstrates the power of `find` for locating files, even in deeply nested or obfuscated directories.

4.  **War Games Script:**  briefly mention the specific lines from the movie script that are relevant:

    *   "GREETINGS PROFESSOR FALKEN." (Initial prompt)
    *   "SHALL WE PLAY A GAME?" (User input)
    *   "HOW ABOUT GLOBAL THERMONUCLEAR WAR?" (User input)
    *   "WOULDN'T YOU PREFER A GOOD GAME OF CHESS?" (System response, leading to the next step)
    * The selection of sides.
    * "Las Vegas"

5.  **Wumpus Game:**  explains the Wumpus game rules, or at least a search query like: `hunt the wumpus game rules adjacent rooms`

6.  **`less` Command:**  identify that `less` is used. The `less` command is a pager, similar to `more`, but with more features. The `:e` command in `less` allows you to examine (edit) a new file.This explains *why* `:e` works.

7.  **Dungeon Game (Zork) - GDT:**  the `GDT` command. briefly explain:  "GDT is a debug command in Zork/Dungeon that allows you to access developer tools.  `DT` likely stands for 'Display Text' or something similar."

8.  **Debug Server (JSON):**  used `curl` and `python -mjson.tool`, meaning, This command uses Python's built-in JSON module to pretty-print the JSON output, making it more readable.

9.  **Banner Ad Server (MeteorMiner):**  Tampermonkey and the MeteorMiner script.  Provided links:

    *   Tampermonkey:  [tampermonkey](https://www.tampermonkey.net/)
    *   MeteorMiner: (You'd need to find the original source, as the SANS link covers the *concept*, but doesn't provide the script itself. If you can't find the original, you could include a simplified version of the script, with a disclaimer that it's adapted from the original.)

10. **Uncaught Exception Handler Server (LFI):** used `php://filter`, meaning PHP's `php://filter` stream wrapper allows you to apply filters to a stream before reading or writing. `convert.base64-encode` encodes the file contents as Base64, preventing the PHP interpreter from executing the code and instead returning the source.

11. **Mobile Analytics (Git):** used `wget --mirror`, meaning `--mirror` creates a local mirror of the remote directory, downloading all files and subdirectories.

12. **Audacity Steps:** Audacity settings (Effect > Change Tempo) or a more precise description, such as:

    *  In Audacity, I combined all the audio tracks.  Then, I selected the entire combined track and used `Effect > Change Tempo`. I increased the tempo by 500%, then applied `Effect > Change Tempo` again with a 400% increase, and finally one more time with a 100% increase.