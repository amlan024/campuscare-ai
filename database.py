
import streamlit as st
from supabase import create_client


@st.cache_resource
def get_database_client():
    """Create the private, server-side administrator client."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


@st.cache_resource
def get_public_database_client():
    """Create a public client restricted by Supabase RLS."""
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_ANON_KEY"]
    return create_client(url, key)


def create_table():
    """Verify that the administrator can access the feedback table."""
    try:
        (
            get_database_client()
            .table("feedback")
            .select("id")
            .limit(1)
            .execute()
        )
    except Exception as exc:
        raise RuntimeError(
            "Could not connect to the CampusCare AI feedback database. "
            "Check the Supabase configuration and table permissions."
        ) from exc



def save_feedback(issue, description, suggested_category, suggested_priority):
    """Save feedback using the private administrator client."""
    response = (
        get_database_client()
        .table("feedback")
        .insert({
            "issue": issue,
            "description": description,
            "suggested_category": suggested_category,
            "suggested_priority": suggested_priority,
        })
        .execute()
    )
    return response.data




def save_feedback_public(
    issue, description, suggested_category, suggested_priority
):
    """Insert student feedback without returning database rows."""
    response = (
        get_public_database_client()
        .table("feedback")
        .insert(
            {
                "issue": issue,
                "description": description,
                "suggested_category": suggested_category,
                "suggested_priority": suggested_priority,
            },
            returning="minimal",
        )
        .execute()
    )
    return response.data



def get_all_feedback():
    """Return feedback records newest first (administrator only)."""
    response = (
        get_database_client()
        .table("feedback")
        .select(
            "id, issue, description, suggested_category, "
            "suggested_priority, created_at"
        )
        .order("id", desc=True)
        .execute()
    )

    return [
        (
            record["id"],
            record["issue"],
            record["description"],
            record.get("suggested_category") or "Other",
            record.get("suggested_priority") or "Normal",
            record["created_at"],
        )
        for record in response.data
    ]


def get_feedback_category_counts():
    """Count feedback records by suggested category (administrator)."""
    from collections import Counter

    response = (
        get_database_client()
        .table("feedback")
        .select("suggested_category")
        .execute()
    )

    counts = Counter(
        record.get("suggested_category") or "Other"
        for record in response.data
    )

    return sorted(counts.items(), key=lambda item: item[1], reverse=True)


def get_feedback_priority_counts():
    """Count feedback records by suggested priority (administrator)."""
    from collections import Counter

    response = (
        get_database_client()
        .table("feedback")
        .select("suggested_priority")
        .execute()
    )

    counts = Counter(
        record.get("suggested_priority") or "Normal"
        for record in response.data
    )

    return sorted(counts.items(), key=lambda item: item[1], reverse=True)
