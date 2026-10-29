import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost ----------
def test_monthly_plan():
    assert membership_cost("monthly", 30, False, False) == 1500

def test_unknown_plan():
    with pytest.raises(ValueError):
        membership_cost("weekly", 30, False, False)

def test_too_young():
    with pytest.raises(ValueError):
        membership_cost("monthly", 10, False, False)

def test_senior_discount():
    assert membership_cost("monthly", 65, False, False) == 1125      # 1500 - 375

def test_student_discount():
    assert membership_cost("quarterly", 20, True, False) == 3600     # 4000 - 400

def test_trainer_yearly():
    assert membership_cost("yearly", 30, False, True) == 13500       # 12000 + 2000 - 500


# ---------- can_enter ----------
def test_can_enter():
    assert can_enter(10, True, False, "M") is True

def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False

def test_outside_hours():
    assert can_enter(3, True, False, "M") is False

def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True


# ---------- bmi_category ----------
def test_bmi_invalid_height():
    with pytest.raises(ValueError):
        bmi_category(70, 0)

def test_bmi_underweight():
    assert bmi_category(45, 1.75) == "underweight"

def test_bmi_normal():
    assert bmi_category(65, 1.75) == "normal"

def test_bmi_overweight():
    assert bmi_category(80, 1.75) == "overweight"

def test_bmi_obese():
    assert bmi_category(100, 1.75) == "obese"


# ================= Extra tests for BRANCH coverage =================
# membership_cost
def test_trainer_non_yearly_plan():          # with_trainer True, plan != "yearly"  (16 -> 18)
    assert membership_cost("monthly", 30, False, True) == 3500

def test_senior_and_student_only_senior_applies():   # age>=60 wins over student (elif skipped)
    assert membership_cost("monthly", 65, True, False) == 1125

def test_age_boundary_14_allowed():
    assert membership_cost("monthly", 14, False, False) == 1500

def test_age_boundary_13_rejected():
    with pytest.raises(ValueError):
        membership_cost("monthly", 13, False, False)

def test_age_boundary_60_gets_senior_discount():
    assert membership_cost("monthly", 60, False, False) == 1125

# can_enter
def test_hour_too_late():
    assert can_enter(23, True, False, "M") is False

def test_hour_lower_boundary_5():
    assert can_enter(5, True, False, "M") is True

def test_hour_upper_boundary_22():
    assert can_enter(22, True, False, "M") is True

def test_women_only_slot_male_denied():
    assert can_enter(10, True, True, "M") is False

def test_non_women_slot_female_allowed():
    assert can_enter(10, True, False, "F") is True

# bmi_category
def test_bmi_negative_height():
    with pytest.raises(ValueError):
        bmi_category(70, -1.7)
