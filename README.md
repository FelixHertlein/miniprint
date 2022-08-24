# miniprint
Print a minified version of your document such as bachelor, master, or PhD thesis!

This projects provides a script which concatenates pages in a 4 by 4 grid and reorders them to reduce the workload after printing the minified document.





## Requirements

- Python 3

## Steps

1. Clone repository `git clone git@github.com:FelixHertlein/miniprint.git`
2. Install requirements  `pip3 install -r requirements.txt`
3. Save your source document in the same folder and rename it to `input.pdf`
4. Run the script using `python3 minify.py`
   - The script generates a file `minified.pdf`
5. Print the `minified.pdf` document at the highest resolution possible
   - Make sure print double page with flipping on the long edge
   - Disable zooming
6. Cut all the sheets at once in a 4 by 4 grid
   - Individual parts have the size A8 (52 mm x 74 mm)
7. Stack all stacks of parts starting from the top-left row-wise until the bottom-right stack
8. Remove empty parts at the end of the stack (optional)
9. Add cover sheets (optional)
10. Glue the whole stack of parts together at the left  edge