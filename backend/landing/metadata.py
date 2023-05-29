HERO_HEADER_METADATA = {
    "autoform_label": "Hero Section",
    "long_description": "This model represents a hero section, which is typically the top section of a webpage and contains a prominent headline, subheading, and background image.",
    "short_description": "A model for creating hero sections.",
    "pages_associated": {
        "Landing": "/",
    },
    "include_preview": True,
    "icon": "SubtitlesIcon",
    "icon_class": None,
    "slug": "hero",
    "tags": ["Landing", "Hero", "Company"],
    "related_components": ["Hero"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "This model represents a hero section, which is typically the top section of a webpage and contains a prominent headline, subheading, and background image.",
        "fields": {
            "Header": "The title of the hero section.",
            "Subheader": "The subtitle of the hero section.",
            "Description": "The description of the hero section.",
            "Button Text": "The text that will appear on the hero section's button.",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "HeroBlock model reference": "/docs/model/heroblock/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "name",
        "id",
    ],
    "allowed": True,
}


SECTION_HEADER_METADATA = {
    "autoform_label": "Section Heading",
    "long_description": "A section heading with a title, subtitle, and description to be used as a heading for various content sections.",
    "short_description": "Section Heading",
    "pages_associated": {
        "Landing": "/",
        "Services": "/services",
    },
    "include_preview": True,
    "icon": "TitleIcon",
    "icon_class": None,
    "slug": "section-title",
    "tags": ["About", "Title", "Content", "Company"],
    "related_components": ["TitleBlock"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "This model represents a section heading with a title, subtitle, and description to be used as a heading for various content sections.",
        "fields": {
            "Name": "A unique name for the section heading.",
            "Header Text": "The main heading text of the section heading.",
            "Subheader Text": "The subheading text of the section heading.",
            "Description": "A brief description of the section heading.",
            "Alignment": "The alignment of the section heading (left, right, or center).",
            "Show Divider": "Whether to show a divider line under the section heading or not.",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "TitleBlock model reference": "/docs/model/titleblock/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "name",
        "title",
        "id",
    ],
    "allowed": True,
}


PROCESS_METADATA = {
    "autoform_label": "Process Step",
    "long_description": "This model represents a collection of steps that describe the process of how the business works. Each step includes a title, description, and an icon to illustrate the step.",
    "short_description": "Model for company process steps",
    "pages_associated": {
        "Landing": "/",
        "Services": "/services",
    },
    "include_preview": True,
    "icon": "AccountTreeIcon",
    "icon_class": None,
    "slug": "header",
    "tags": ["Landing" "Process", "Company"],
    "related_components": ["Header"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "This model represents a collection of steps that describe the process of how the business works.",
        "fields": {
            "Header": "The title of the process step",
            "Description": "A brief description of the process step",
            "Icon": "The icon that represents the process step",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "Process model reference": "/docs/model/process/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "title",
        "id",
    ],
    "allowed": True,
}


HERO_METADATA = {
    "autoform_label": "Hero",
    "long_description": "This model represents the hero section of a landing page.",
    "short_description": "Hero section of landing page",
    "pages_associated": {
        "Landing": "/",
        "Services": "/services",
    },
    "include_preview": True,
    "icon": "AccountTreeIcon",
    "icon_class": "text-primary",
    "slug": "hero",
    "tags": ["landing", "hero"],
    "related_components": ["HeroBlock"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "This model is used to store the hero section of a landing page.",
        "fields": {
            "Name": "The name of the hero section.",
            "Contact": "The contact information to display in the hero section.",
            "Social": "The social media links to display in the hero section.",
            "Hero Block": "The hero block to use in the hero section.",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "name",
        "id",
    ],
    "allowed": True,
}


PROCESSES_METADATA = {
    "autoform_label": "Processes",
    "long_description": "A collection of related process steps.",
    "short_description": "A collection of related process steps.",
    "pages_associated": {
        "Landing": "/",
        "Services": "/services",
    },
    "include_preview": True,
    "icon": "AccountTreeIcon",
    "icon_class": None,
    "slug": "processes",
    "tags": ["processes", "workflow"],
    "related_components": ["ProcessStep"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "Represents a collection of related process steps.",
        "fields": {
            "Name": "The name of the process collection.",
            "Processes": "The process steps included in the collection.",
            "Title Block": "The title block used to display the process collection on a page.",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "Process model reference": "/docs/model/process/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "name",
        "id",
    ],
    "allowed": True,
}


LATEST_NEWS_METADATA = {
    "autoform_label": "Latest News",
    "long_description": "A model to showcase the latest news articles on the landing page.",
    "short_description": "Model to showcase the latest news articles.",
    "pages_associated": {
        "Landing": "/",
    },
    "include_preview": True,
    "icon": "AccountTreeIcon",
    "icon_class": None,
    "slug": "latest-news",
    "tags": ["news", "landing", "articles"],
    "related_components": ["LatestNewsComponent"],
    "visibility": True,
    "access_level": "All",
    "info_dump": {
        "purpose": "To showcase the latest news articles on the landing page.",
        "fields": {
            "name": "The name of the LatestNews instance.",
            "latest_articles": "The related Articles instances to showcase as the latest news.",
            "title_block": "The related TitleBlock instance to use as the title of the LatestNews section on the landing page.",
        },
        "model_links": {
            "Django documentation": "https://docs.djangoproject.com/en/3.2/topics/db/models/",
            "Landing app documentation": "/docs/app/landing/",
        },
    },
    "filter_options": [
        "name",
        "id",
    ],
    "allowed": True,
}
