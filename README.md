# OpenWanderer Face and License Plate Anonymizer

This is an experimental application to obfuscate faces and license plates in OpenWanderer projects. Note that it makes use of these existing anonymisers:

- [understand.ai Anonymizer](https://github.com/understand-ai/anonymizer)
- [Tyndare blur_persons](https://github.com/tyndare/blur-persons)

Both these libraries are included in this repository for easy installation; I have also modified their code slightly to make it work with this application. The code from these repositories was taken in autumn 2020 (as at Feb 2022, this remains the most recent version for both). 

Please see the individual licensing for the two anonymiserd. The rest of the code is the OpenWanderer project's own code and is licensed under the LGPL.

## What does it do?

It finds all unauthorised panoramas in an [OpenWanderer](https://github.com/opemwanderer/openwanderer) database, and attempts to anonymise them, using one of the above anonymisers. Optionally, you can specify a range of pano IDs in the database to anonymise.

## Installation

(Taken from the instructions for [understand.ai Anonymizer](https://github.com/understand-ai/anonymizer) and modified)

To install the anonymizer just clone this repository, create a new Python virtual environment and install the dependencies.  
The sequence of commands to do all this is

```bash
python3 -m venv ~/.virtualenvs/anonymizer
source ~/.virtualenvs/anonymizer/bin/activate

git clone https://github.com/openwanderer/anon.git

pip3 install -r requirements.txt
```

## Usage

```bash
python3 anon.py [-a anonymiser] [-f startPanoID] [-t endPanoID] [-a anonymizer] -i InputImageDirectory -o OutputImageDirectory
```

- The `anonymiser` should be either `understandai` (default) or `blur_persons`.
- `startPanoID` and `endPanoID` define the range of panorama IDs in the database to anonymise. If not specified, all unauthorised panoramas will be anonymised.
- `InputImageDirectory` is the location of the unanonymised images.
- `OutputImageDirectory` is the location to write out the anonymised images

## Performance

Of the two, `blur_persons` is the most effective, anonymising almost all visible faces and cars. However it blurs the whole car, not just the license plate - which is not ideal, and critically, it is very slow, taking several minutes to anonymise one panorama.

`understandai` is much faster, taking a few seconds to anonymise panoramas, and does work on the majority of cases though might miss faces and license plates which are some distance away from the camera. It does only blur the license plate, not the whole car, which is an advantage.
