# bulk-certificate-sender

Send many certificates to many emails. This script mean to be used with my [bulk-certificate-generator](https://github.com/fiqrisr/bulk-certificate-generator) script.

## Usage

Put list of names and emails in `email_list.txt` and certificates generated by [bulk-certificate-generator](https://github.com/fiqrisr/bulk-certificate-generator) script inside `input` folder. Don't forget to put email body into `body_template.txt`.

Open `config.cfg` and set SMTP host, port, email subject, and your login credentials then run the script.

```bash
python main.py
```

## Configuration

See `config.cfg` (self-explanatory).

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0)
