# image download

a python test task
### Task: 
Given a plaintext file containing URLs, one per line, e.g.:  
http://mywebserver.com/images/271947.jpg  
http://mywebserver.com/images/24174.jpg  
http://somewebsrv.com/img/992147.jpg  
Write a script that takes this plaintext file as an argument and downloads all images, storing them on the local hard disk.  

### Sollution comments:
* all downloaded images are stored in 'img' dir  
* to avoid name collision, images are named with their full url  

## Run

```
python savepic.py <text-file-with-ULRs>
```

## Tests

```
python test.py -b
```

## Author

**Sergey Sambor** - [mooromets](https://github.com/mooromets)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
