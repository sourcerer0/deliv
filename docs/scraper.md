# Scraper
## Scraper
### Parameters
```
kwargs['data'] (string): Data to be submitted
```

### Attributes
#### self.data
```
- Description: Data to be submitted
- Type: string
```

#### self.URL
```
- Description: API / Service
- Type: string
```

#### self.log
```
- Description: Logs. Replied information over time.
- Type: list
```

### Methods
#### set_tracking_url()
```
- Description: URL setter. Not a property
- Parameters: URL
- Return: None
```

#### check_new_info()
```
- Description: Get information from API or Service
- Parameters: None
- Return: Every information not present at self.log
```

## Correios
### Basic Usage
```python
from deliv import Correios

myPackage = Correios(data="<your package tracking code here>")

# print(myPackage.URL)

# In Correios class and others child classes, __init__ calls set_tracking_url()

for info in myPackage.check_new_info(): print(info)

```

## Cep
### (New) Attributes
#### self.adress
```
- Description: Locator instantiated according to address returned from API / Service
- Type: Locator Class
```

### Basic Usage
```python
from deliv import Cep

myAddr = Cep(data="<your CEP code here (ZIP if you're from US)>")

myAddr.check_new_info()
# check_new_info returns address, but keeps self.log empty
# for inf in myAddr.check_new_info(): print(inf) // to see returned data

myAddr.address.location #detailed

myAddr.address.human_time #current time in UTC

myAddr.address.set_timezone() #finds a probable timezone for your adddress

myAddr.address.human_time #current time in your timezone

print(myAddr.address.up_time()) #when Location was instantiated

```

