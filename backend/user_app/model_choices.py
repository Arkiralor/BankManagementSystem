class UserModelChoices:
    user = "User"
    accountant = "Accountant"
    admin = "Administrator"

    USER_TYPE_CHOICES = (
        (user, user),
        (accountant, accountant),
        (admin, admin)
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