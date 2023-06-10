class UserModelChoices:
    teller = "Teller"
    accountant = "Accountant"
    admin = "Administrator"
    moderator = "Moderator"

    USER_TYPE_CHOICES = (
        (accountant, accountant),
        (teller, teller),
        (admin, admin),
        (moderator, moderator)
    )

    female = "Female"
    male = "Male"
    other = "Other"

    USER_GENDER_CHOICES = (
        (female, female),
        (male, male),
        (other, other)
    )

    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

    ALLOWED_FILE_EXTENSIONS = (PNG, JPG, JPEG, PNG)

class AddressChoices:
    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

    ALLOWED_FILE_EXTENSIONS = (PNG, JPG, JPEG, PNG)