export class User {
    fullname:string;
    bio:string;
    birthday:string;
    gender:string;

    constructor(fullname:string, bio:string, birthday:string, gender:string) {
        this.fullname = fullname;
        this.bio = bio;
        this.birthday = birthday;
        this.gender = gender;
    }
}
