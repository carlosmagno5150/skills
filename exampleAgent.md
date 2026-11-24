# Agent Notes  
  
## Project Shape  
- Solution: `jc-corretora.sln` with API project `src/JLC.RegisterApi` and tests in `tests/JLC.RegisterApiTests`.  
- API entrypoint is `src/JLC.RegisterApi/Program.cs`; it is currently a minimal ASP.NET Core app with OpenAPI only in Development.  
- Stack from project files: .NET `net10.0`, ASP.NET Core Minimal API, EF Core 9 + Npgsql, xUnit.  
- Main project has `<ImplicitUsings>disable</ImplicitUsings>` and `<Nullable>disable</Nullable>`; test project enables both.  
  
## Commands  
- Restore/build solution: `dotnet restore jc-corretora.sln` then `dotnet build jc-corretora.sln`.  
- Run all tests: `dotnet test jc-corretora.sln`.  
- Run only test project: `dotnet test tests/JLC.RegisterApiTests/JLC.RegisterApiTests.csproj`.  
- Run API locally: `dotnet run --project src/JLC.RegisterApi/JLC.RegisterApi.csproj`.  
  
## Architecture Rules To Preserve  
- Endpoints must not access persistence directly; route work through an application service.  
- Keep business rules out of endpoint/HTTP handler code.  
- Validation errors should return HTTP 400 with `ProblemDetails` and Portuguese messages.  
- New business rules need unit tests; new endpoints need at least one happy-path integration test.  
- Do not add dependencies without a short written justification in the plan/summary.  
  
## Conventions  
- Class and file names in English; user-facing error messages in Portuguese.  
- Commit format when asked to commit: `tipo(escopo): descrição` plus the requirement identifier if one exists.


