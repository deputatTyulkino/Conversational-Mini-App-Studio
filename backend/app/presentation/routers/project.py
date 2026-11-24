from typing import Annotated
from uuid import UUID

from app.application.schemas.entities.project import (
    ProjectCreate,
    ProjectIdRead,
    ProjectRead,
    ProjectUpdate,
    ProjectWithChatsRead,
)
from app.application.services.projects.commands.create_project import (
    CreateProjectService,
)
from app.application.services.projects.commands.delete_project import (
    DeleteProjectService,
)
from app.application.services.projects.commands.update_project import (
    UpdateProjectService,
)
from app.application.services.projects.queries.get_all_project import (
    GetAllProjectService,
    GetPinnedProjectsService,
)
from app.application.services.projects.queries.get_project import GetProjectService
from app.infrastructure.dependencies.entities.projects.command.create_project import (
    create_project_service,
)
from app.infrastructure.dependencies.entities.projects.command.delete_project import (
    delete_project_service,
)
from app.infrastructure.dependencies.entities.projects.command.update_project import (
    update_project_service,
)
from app.infrastructure.dependencies.entities.projects.queries.get_all_project import (
    get_all_project_service,
    get_pinned_project_service,
)
from app.infrastructure.dependencies.entities.projects.queries.get_project import (
    get_project_service,
)
from app.presentation.api.schemas.responses import SuccessResponse
from fastapi import APIRouter, Depends, status

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get(
    "",
    response_model=SuccessResponse[list[ProjectWithChatsRead]],
    status_code=status.HTTP_200_OK,
)
async def get_all_projects_endpoint(
    get_all_projects: Annotated[GetAllProjectService, Depends(get_all_project_service)],
):
    data = await get_all_projects()
    return SuccessResponse(data=data)


@router.get(
    "/pinned",
    response_model=SuccessResponse[list[ProjectWithChatsRead]],
    status_code=status.HTTP_200_OK,
)
async def get_pinned_projects_endpoint(
    get_pinned_projects: Annotated[
        GetPinnedProjectsService, Depends(get_pinned_project_service)
    ],
):
    data = await get_pinned_projects()
    return SuccessResponse(data=data)


@router.get(
    "/{project_id}",
    response_model=SuccessResponse[ProjectWithChatsRead],
    status_code=status.HTTP_200_OK,
)
async def get_project_endpoint(
    project_id: UUID,
    get_project: Annotated[GetProjectService, Depends(get_project_service)],
):
    data = await get_project(project_id)
    return SuccessResponse(data=data)


@router.post(
    "",
    response_model=SuccessResponse[ProjectRead],
    status_code=status.HTTP_201_CREATED,
)
async def create_project_endpoint(
    project_data: ProjectCreate,
    create_project: Annotated[CreateProjectService, Depends(create_project_service)],
):
    data = await create_project(project_data)
    return SuccessResponse(data=data)


@router.patch(
    "/{project_id}",
    response_model=SuccessResponse[ProjectRead],
    status_code=status.HTTP_200_OK,
)
async def update_project_endpoint(
    project_id: UUID,
    project_data: ProjectUpdate,
    update_project: Annotated[UpdateProjectService, Depends(update_project_service)],
):
    data = await update_project(project_id, project_data)
    return SuccessResponse(data=data)


@router.delete(
    "/{project_id}",
    response_model=SuccessResponse[ProjectIdRead],
    status_code=status.HTTP_200_OK,
)
async def delete_project_endpoint(
    project_id: UUID,
    delete_project: Annotated[DeleteProjectService, Depends(delete_project_service)],
):
    data = await delete_project(project_id)
    return SuccessResponse(data=data)
