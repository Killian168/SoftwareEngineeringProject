import * as libphonenumber from 'google-libphonenumber';

export class Country {
  iso: string;
  name: string;
  code: string;
  sampleMobilePhone: string;
  sampleFixedPhone: string;

  constructor(iso: string, name: string) {
    this.iso = iso;
    this.name = name;

    const phoneUtil = libphonenumber.PhoneNumberUtil.getInstance();
    const PNF = libphonenumber.PhoneNumberFormat;
    const PNT = libphonenumber.PhoneNumberType;
    const countryExampleMobileNumber = phoneUtil.getExampleNumberForType(this.iso, PNT.MOBILE);
    const countryExampleFixedNumber = phoneUtil.getExampleNumberForType(this.iso, PNT.FIXED_LINE);

    if (countryExampleMobileNumber) {
      const exampleMobileNumberFormatted = phoneUtil.format(countryExampleMobileNumber, PNF.NATIONAL);
      const exampleFixedNumberFormatted = phoneUtil.format(countryExampleFixedNumber, PNF.NATIONAL);
      this.sampleMobilePhone = exampleMobileNumberFormatted;
      this.sampleFixedPhone = exampleFixedNumberFormatted;
      this.code = '+' + countryExampleMobileNumber.getCountryCode();
    }
  }
}
