from database.enum import IntegrationTypeEnum
from services.integrations.airtable import AirTableIntegrationProcessor
from services.integrations.hubspot import HubSpotIntegrationProcessor
from services.integrations.notion import NotionIntegrationProcessor
from utils.integrations import IntegrationProcessor


integration_processors: dict[IntegrationTypeEnum, type[IntegrationProcessor]] = {
    IntegrationTypeEnum.HUBSPOT: HubSpotIntegrationProcessor,
    IntegrationTypeEnum.AIRTABLE: AirTableIntegrationProcessor,
    IntegrationTypeEnum.NOTION: NotionIntegrationProcessor,
}
