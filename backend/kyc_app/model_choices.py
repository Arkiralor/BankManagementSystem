class CustomerChoice:
    pan_card = "PAN Card"
    aadhaar_card = "Aadhar Card"
    voter_id = "Voter ID"
    electricity_bill = "Electricity Bill"
    passport = "Passport"
    driving_license = "Driving License"

    ID_PROOF_CHOICES = (
        (pan_card, pan_card),
        (aadhaar_card, aadhaar_card),
        (voter_id, voter_id),
        (passport, passport),
        (driving_license, driving_license)
    )

    ADDRESS_PROOF_CHOICES = (
        (aadhaar_card, aadhaar_card),
        (voter_id, voter_id),
        (electricity_bill, electricity_bill),
        (passport, passport),
        (driving_license, driving_license)
    )

    PDF = "pdf"
    JPG = "jpg"
    JPEG = "jpeg"
    PNG = "png"

    ALLOWED_FILE_EXTENSIONS = (PNG, JPG, JPEG, PNG)