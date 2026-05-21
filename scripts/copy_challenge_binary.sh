key="$HOME/Desktop/projects/pwn-college-learning/key"
read -p "Binary name: " binary
read -p "Destination: " dest

# Make sure the binary is copied to the tmp dir on dojo machine first
scp -i $key hacker@dojo.pwn.college:/tmp/$binary $dest
